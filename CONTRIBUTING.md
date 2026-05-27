# Contributing

Small, focused PRs welcome.

## Quick start

```bash
git clone https://github.com/ademczuk/modulewarden-website
cd modulewarden-website
python -m http.server 8080
# edit index.html, refresh
```

## What to submit

- Copy fixes (typos, clearer phrasing)
- New citations (with real source links)
- New FAQ items (real questions from real conversations)
- Pricing tier tweaks
- New integration sections
- Accessibility improvements (contrast, focus rings, ARIA labels)

## What to discuss in an issue first

- New pages (blog, docs, changelog)
- Framework migration (Next.js, Astro)
- Heavy redesign
- New dependencies

## Style

- American English
- No em-dashes
- No arrow glyphs in copy
- Sentence fragments OK in marketing bullets
- Cite real sources, not placeholders

## Marker check before pushing

The repo follows a strict no-AI-marker policy on visible copy. Before committing changes to `index.html`, save this as `scripts/check-markers.py` and run it:

```python
import re, sys
text = open('index.html', encoding='utf-8').read()
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
banned_chars = {
    'em-dash': '—', 'en-dash': '–',
    'right-arrow': '→', 'left-arrow': '←',
    'lsquo': '‘', 'rsquo': '’',
    'ldquo': '“', 'rdquo': '”',
    'ellipsis': '…',
}
hits = {n: text.count(c) for n, c in banned_chars.items() if text.count(c)}
banned_words = r'\b(comprehensive|delv(e|es|ing)|tapestry|realm|embark|leverag(e|ed|ing)|nuanced|holistic|seamless|landscape|journey|vibrant|unveil)\b'
word_hits = re.findall(banned_words, text, re.I)
if hits or word_hits:
    print(f'BLOCKED: chars={hits} words={word_hits}')
    sys.exit(1)
print('CLEAN')
```

Should print `CLEAN`. If it blocks, replace the offending chars or words before pushing.
