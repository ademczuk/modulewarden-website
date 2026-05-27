# modulewarden-website

Static marketing site for [ModuleWarden](https://github.com/apetersson/ModuleWarden), the policy layer that gates npm packages before they install.

**Live:** https://ademczuk.github.io/modulewarden-website/

## What is in here

| File | Purpose |
|------|---------|
| `index.html` | The full landing page. Single file. Tailwind via CDN. No build step. |
| `_headers` | Security headers (HSTS, XFO, etc.) for Cloudflare Pages / Netlify. |
| `.github/workflows/pages.yml` | Deploys to GitHub Pages on every push to `main`. |
| `LICENSE` | MIT. |
| `CONTRIBUTING.md` | Style rules + marker-check script. |

## Local preview

```bash
python -m http.server 8080
# open http://localhost:8080
```

No build, no install, no node_modules. Edit `index.html` and refresh.

## Deploy

### GitHub Pages (default, already wired)

Push to `main`. The workflow at `.github/workflows/pages.yml` builds and deploys automatically. URL: https://ademczuk.github.io/modulewarden-website/

First-time setup on a fresh clone:

1. Settings > Pages > Build and deployment > Source: **GitHub Actions**
2. The next push to `main` triggers the workflow.

### Cloudflare Pages (recommended for a custom domain)

```bash
npx wrangler pages deploy . --project-name=modulewarden
```

Then add `modulewarden.com` as a custom domain in the Cloudflare dashboard. SSL auto-provisions.

### Vercel

```bash
npx vercel --prod
```

### Netlify

```bash
npx netlify-cli deploy --dir=. --prod
```

## Wiring the early-access form

The form posts to a placeholder endpoint. Pick one and replace `REPLACE_WITH_YOUR_FORM_ID` in `index.html`:

- **Formspree** (fastest, free tier): https://formspree.io
- **Buttondown** (mailing list): https://buttondown.com
- **Cloudflare Worker** (self-hosted, free, scales): template below
- **Plain mailto** (degraded fallback): change `<form action="..." method="POST">` to `<form action="mailto:hi@modulewarden.com" method="POST" enctype="text/plain">`

### Cloudflare Worker form handler (template)

Save as `workers/form.js`, deploy with `wrangler deploy`, then update the form `action` attribute in `index.html` to your worker URL.

```js
export default {
  async fetch(req, env) {
    if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });
    const form = await req.formData();
    const body = {
      email: form.get('email'),
      company: form.get('company'),
      team_size: form.get('team_size'),
      worry: form.get('worry'),
      ts: new Date().toISOString(),
    };
    await env.SIGNUPS.put(crypto.randomUUID(), JSON.stringify(body));
    if (env.SLACK_WEBHOOK) {
      await fetch(env.SLACK_WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `New signup: ${body.email} (${body.company || 'no company'})` }),
      });
    }
    return Response.redirect('https://modulewarden.com/?signup=ok', 303);
  },
};
```

Then:

```bash
wrangler kv namespace create SIGNUPS
# bind SIGNUPS in wrangler.toml
wrangler secret put SLACK_WEBHOOK
```

## Editing the page

The page is one file. Common edits:

| Looking for | Search in `index.html` |
|-------------|------------------------|
| Hero headline | `Stop trusting your` |
| Pricing tiers | `id="pricing"` |
| FAQ items | `id="faq"` |
| Big stats | `847K` |
| Terminal demo | `npm install postmark-mcp` |
| Early-access form | `id="early"` |

Tailwind classes are inline. No CSS file to track down.

## Adding pages

For a second page (blog, docs, changelog) add it at the repo root as `blog.html` or under a folder `docs/index.html`. The GitHub Actions workflow uploads everything in the repo root by default. Pages will serve `/blog.html` and `/docs/` automatically.

## Custom domain

Add a `CNAME` file at the repo root containing your domain (e.g. `modulewarden.com`). Then in your DNS provider, point an A or ALIAS record at the GitHub Pages IPs. For the apex domain, the cleanest path is Cloudflare proxying.

## Style rules

- American English throughout
- No em-dashes (use hyphens, commas, or full stops)
- No arrow glyphs in copy (use words: "then", "to")
- Citations are real and dated. Refresh as new incidents land.

Run the marker-check script in `CONTRIBUTING.md` before pushing copy changes.

## Related

- [github.com/apetersson/ModuleWarden](https://github.com/apetersson/ModuleWarden), the actual product (private during development)
- [Sonatype Open-Source Malware Index Q2 2025](https://www.sonatype.com/press-releases/q2-2025-open-source-malware-index), source for the 847K and 156% YoY stats
- [Snyk postmark-mcp writeup](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/), the incident shown in the hero terminal demo
- [github.com/perplexityai/bumblebee](https://github.com/perplexityai/bumblebee), Bumblebee scanner referenced in the integrations section
