# ModuleWarden pitch video, verbatim narration (v2, re-dub)

The exact words to speak in `demo/ModuleWarden_pitch.mp4` (female voice, Kokoro
af_bella or a human re-dub). Read unhurried, around 140 words per minute, with a
short beat of silence between blocks. The honesty beat was cut for pacing; the
honest framing still lands in block 8 ("detection stays with the gate") and block
12 ("conceded the rest with the data"). One block per shot, in order.

1. Title. ModuleWarden, by Team Andrew.

2. Supply chain. Your supply chain is code you did not write, running on every machine you ship to.

3. The threat. A package you trust ships a new release. The maintainer account is compromised, or a contributor goes rogue. The danger is the delta: what changed between two versions.

4. Compounding risk. And it gets worse fast. Every dependency brings its own. As the tree grows toward thousands, the chance that one of them is an attack vector climbs toward certain. You cannot review them by hand.

5. Guard the registry. So we guard the one interface every package crosses: the registry. You turn it on with a single line, and ModuleWarden audits every new version automatically, before it reaches your code.

6. Evidence first. An agentic reviewer reads the code and lands on one verdict: allow, block, or quarantine. You open the session and read exactly what the model saw.

7. The model. The model is a twenty-seven billion parameter Qwen, fine-tuned on real CVE diffs. We matched each vulnerable version to its fix and trained two LoRA adapters on the Leonardo supercomputer. It is published on Hugging Face.

8. Trained vs untrained. Held-out validation loss zero point two one, token accuracy ninety-four percent. That measures how faithfully it writes up evidence, not whether it spots danger. Untuned, the base drifts the schema; tuned, it is valid every time. Detection stays with the gate.

9. The forecast, two signals. We ship the forecast. We send each package's download history to Sybilion and use two things: the slope, to rank what we review first, and the band width, to route it. Too wide to call goes to a human; a tight band, the gate auto-audits.

10. Live at scale. We ran it live across forty-six packages. Semver and minimatch are the same size, but the forecast separates them. Semver's band is tight, it auto-clears. Minimatch's is wide, a human looks. Eighteen routed, twenty-eight cleared.

11. The threat from within. And the most dangerous attacker is not always on the outside. Verizon puts seventy-four percent of breaches on the human element: a developer in a hurry, an AI assistant suggesting a package. ModuleWarden gates the install no matter who runs it. That is the threat from within, and it is the one we close.

12. Close. Sybilion says the domain is yours. We kept what the forecast earned, trajectory ranking. We gated what it could not, and conceded the rest with the data. That is how you grow a forecast without it lying to you.

13. Tagline. ModuleWarden. Audit every version. Forecast every trajectory. Show every piece of evidence.
