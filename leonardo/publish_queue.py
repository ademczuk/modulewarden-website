#!/usr/bin/env python3
"""Poll the Leonardo reservation and write leonardo/queue.json for the website.

Runs either from a GitHub Actions runner (credentials in LEONARDO_USER /
LEONARDO_PASSWORD secrets) or locally by the operator. The emitted JSON is
non-sensitive (Slurm job ids, usernames, node counts) and is what the static
dashboard at leonardo/index.html renders.

Usage:
  LEONARDO_USER=a08trc01 LEONARDO_PASSWORD=... python leonardo/publish_queue.py
  python leonardo/publish_queue.py --out leonardo/queue.json --reservation s_tra_ncc

Requires: paramiko.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys

try:
    import paramiko
except ImportError:
    sys.exit("paramiko is required: pip install paramiko")

DEFAULT_RESERVATION = "s_tra_ncc"
DEFAULT_LOGIN = "login01-ext.leonardo.cineca.it"
GPUS_PER_NODE = 4
FREE_STATES = {"idle", "resv"}
BUSY_STATES = {"mix", "alloc", "comp"}
# Confirmed team accounts get role labels; the rest of the shared tra26_minwinsc
# cohort (the Leonardo group a08trc01/a08trc02 both belong to) is tracked too, so
# no teammate's job is ever missed whatever trainee login they submit from.
ROLES = {"a08trc01": "devops/decepticon", "a08trc02": "finetune/petersson"}
COHORT = [
    "a08trc01", "a08trc02", "a08trc0e", "a08trc0r", "a08trc0v", "a08trc0x",
    "a08trc11", "a08trc13", "a08trc14", "a08trc16", "a08trc17", "a08trc21",
    "a08trc22", "a08trc23",
]
FMT = "%i|%u|%T|%D|%M|%l|%r|%R|%S"


def load_creds() -> tuple[str, str, str]:
    user = os.environ.get("LEONARDO_USER")
    pw = os.environ.get("LEONARDO_PASSWORD") or os.environ.get("LEONARDO_PASS")
    login = os.environ.get("LEONARDO_LOGIN", DEFAULT_LOGIN)
    if not (user and pw):
        for p in (
            pathlib.Path(__file__).resolve().parents[2] / "ModuleWarden" / ".leonardo-access",
            pathlib.Path(__file__).resolve().parents[2] / ".leonardo-access",
            pathlib.Path.home() / ".leonardo-env",
        ):
            if p.is_file():
                kv = {}
                for line in p.read_text().splitlines():
                    if "=" in line and not line.strip().startswith("#"):
                        k, v = line.split("=", 1)
                        kv[k.strip()] = v.strip().strip("'\"")
                user = user or kv.get("LEONARDO_USER") or kv.get("USERNAME")
                pw = pw or kv.get("LEONARDO_PASSWORD") or kv.get("PASSWORD")
                break
    if not (user and pw):
        sys.exit("No credentials: set LEONARDO_USER and LEONARDO_PASSWORD.")
    return user, pw, login


def parse_jobs(text: str, accounts: set[str]) -> list[dict]:
    keys = ["id", "user", "state", "nodes", "time", "limit", "reason", "where", "start"]
    out = []
    for line in text.splitlines():
        parts = line.rstrip("\n").split("|")
        if len(parts) >= len(keys) and parts[0] and parts[0] != "JOBID":
            j = dict(zip(keys, parts))
            j["mine"] = j["user"] in accounts
            j["role"] = ROLES.get(j["user"], j["user"])
            out.append(j)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reservation", default=DEFAULT_RESERVATION)
    ap.add_argument("--accounts", default=",".join(COHORT))
    ap.add_argument("--out", default=str(pathlib.Path(__file__).with_name("queue.json")))
    args = ap.parse_args()
    accounts = {a.strip() for a in args.accounts.split(",") if a.strip()}

    user, pw, login = load_creds()
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(login, username=user, password=pw, timeout=25,
              allow_agent=False, look_for_keys=False)

    def run(cmd: str) -> str:
        _, o, _ = c.exec_command(cmd, timeout=35)
        return o.read().decode(errors="replace")

    res_raw = run(f"scontrol show reservation {args.reservation} 2>&1")
    if "ReservationName" not in res_raw:
        c.close()
        sys.exit(f"reservation {args.reservation} not found: {res_raw.strip()[:200]}")
    f = dict(re.findall(r"(\w+)=([^\s]+)", res_raw))
    nodes_expr = f.get("Nodes", "")

    epochs = run(
        f'echo NOW=$(date +%s); '
        f'echo END=$(date -d "{f.get("EndTime","")}" +%s 2>/dev/null)'
    )
    now_epoch = end_epoch = None
    for line in epochs.splitlines():
        if line.startswith("NOW=") and line[4:].strip().isdigit():
            now_epoch = int(line[4:].strip())
        if line.startswith("END=") and line[4:].strip().isdigit():
            end_epoch = int(line[4:].strip())

    nodes = []
    if nodes_expr:
        for line in run(f"sinfo -N -n '{nodes_expr}' -h -o '%N|%t' 2>/dev/null").splitlines():
            if "|" in line:
                _, st = line.split("|", 1)
                nodes.append(st.strip().rstrip("*~#$@+"))
    total = len(nodes)
    free = sum(1 for st in nodes if st in FREE_STATES)
    busy = sum(1 for st in nodes if st in BUSY_STATES)

    team = parse_jobs(run(f"squeue -u {','.join(sorted(accounts))} -h -o '{FMT}' 2>/dev/null"), accounts)
    queue = parse_jobs(run(f"squeue --reservation={args.reservation} -h -S '-t,-Q' -o '{FMT}' 2>/dev/null"), accounts)
    c.close()

    doc = {
        "generated_epoch": now_epoch,
        "reservation": args.reservation,
        "account": f.get("Accounts"),
        "partition": f.get("PartitionName"),
        "state": f.get("State"),
        "start": f.get("StartTime"),
        "end": f.get("EndTime"),
        "end_epoch": end_epoch,
        "nodes": {
            "total": total, "free": free, "busy": busy,
            "other": total - free - busy,
            "free_gpus_est": free * GPUS_PER_NODE,
        },
        "team": team,
        "queue": queue,
    }
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}  (free {free}/{total} nodes, {len(team)} team jobs, {len(queue)} on reservation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
