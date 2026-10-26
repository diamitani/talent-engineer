#!/usr/bin/env python3
"""Render a local candidate snapshot. Does not fetch, host or enforce access control."""
import argparse
import html
import json
import math
import sys
from pathlib import Path
NAMES = {'workday': 'Workday', 'greenhouse': 'Greenhouse', 'gem': 'Gem', 'brighthire': 'BrightHire'}
def esc(value):
    return html.escape('Not provided' if value is None else str(value), quote=True)

def render(data):
    if not isinstance(data, dict): raise ValueError('Expected a JSON object')
    if not isinstance(data.get('candidate'), str) or not data['candidate'].strip():
        raise ValueError('candidate must be a non-empty string')
    if not isinstance(data.get('sections'), dict): raise ValueError('sections must be an object')
    if set(data['sections']) - set(NAMES): raise ValueError('Unknown section key')
    cards, badges = [], []
    for key, title in NAMES.items():
        section = data['sections'].get(key, {'status': 'unavailable', 'reason': 'Not connected or not supplied'})
        if not isinstance(section, dict): raise ValueError(f'{key} section must be an object')
        status = section.get('status', 'unavailable')
        if status not in ('ok', 'unavailable', 'export'): raise ValueError(f'{key}: invalid status')
        available = status in ('ok', 'export')
        label = 'snapshot' if status == 'ok' else ('export, not live' if status == 'export' else 'unavailable')
        badges.append(f'<span class="pill">{title}: {label}</span>')
        if available:
            if not section.get('fetched_at'): raise ValueError(f'{key}: fetched_at required for available data')
            if not isinstance(section.get('items', []), list): raise ValueError(f'{key}: items must be a list')
            rows = []
            for item in section.get('items', []):
                if not isinstance(item, dict) or 'label' not in item or 'value' not in item:
                    raise ValueError(f'{key}: each item needs label and value')
                rows.append(f'<dt>{esc(item["label"])}</dt><dd>{esc(item["value"])}</dd>')
            body = f'<dl>{"".join(rows)}</dl><p class="meta">Fetched: {esc(section["fetched_at"])}</p>'
        else:
            body = f'<p>Not available: {esc(section.get("reason", "Unknown"))}. No data from this system is shown.</p>'
        cards.append(f'<section><h2>{title}</h2>{body}</section>')
    coverage = ''
    cov = data.get('evidence_coverage')
    if cov:
        if not isinstance(cov, dict): raise ValueError('evidence_coverage must be an object')
        covered, total = cov.get('topics_covered'), cov.get('topics_total')
        if any(isinstance(x, bool) or not isinstance(x, int) for x in (covered, total)) or total <= 0 or not 0 <= covered <= total:
            raise ValueError('Coverage requires integers: 0 <= topics_covered <= topics_total; total > 0')
        percent = round(100 * covered / total)
        source, fetched = cov.get('source'), cov.get('fetched_at')
        if not source or not fetched: raise ValueError('Coverage requires source and fetched_at')
        coverage = f'<section><h2>Interview evidence coverage</h2><p>{covered} / {total} rubric topics ({percent}%). This describes evidence completeness, not candidate quality.</p><p class="meta">Source: {esc(source)}. Fetched: {esc(fetched)}</p></section>'
    pending = data.get('open_items', [])
    if not isinstance(pending, list): raise ValueError('open_items must be a list')
    items = ''.join(f'<li>{esc(x)}</li>' for x in pending) or '<li>No open items supplied</li>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>{esc(data['candidate'])} - candidate snapshot</title><style>
body{{font:16px/1.55 system-ui,sans-serif;color:#251f21;background:white;max-width:760px;margin:auto;padding:20px;overflow-wrap:anywhere}} h1{{font-size:26px;line-height:1.2}}h2{{font-size:19px}}section{{border-top:1px solid #eae9ea;padding:12px 0}}.pill{{display:inline-block;background:#f4efec;border-radius:12px;padding:4px 10px;margin:4px 4px 4px 0;font-size:13px}}.meta{{font-size:13px;color:#585254}}dl{{display:grid;grid-template-columns:34% 1fr;gap:8px 16px}}dt{{color:#585254}}dd{{margin:0}}@media(max-width:480px){{dl{{display:block}}dd{{margin:0 0 12px}}}}
</style></head><body><p class="meta">LOCAL SNAPSHOT / NOT ACCESS-CONTROLLED</p><h1>{esc(data['candidate'])}</h1><p>{esc(data.get('role'))}</p><p class="meta">Generated: {esc(data.get('generated'))}. Rebuild to refresh.</p><div>{''.join(badges)}</div>{coverage}{''.join(cards)}<section><h2>Open items</h2><ul>{items}</ul></section><p class="meta">No automatic refresh. A local HTML file is not private hosting. Do not upload real candidate data to public hosting. Deploy only behind company-approved SSO with per-record access controls. No hiring decisions are made here.</p></body></html>'''

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source'); p.add_argument('out_dir')
    args = p.parse_args(argv)
    try:
        data = json.loads(Path(args.source).read_text(encoding='utf-8'))
        page = render(data)
        out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
        dest = out / 'index.html'
        dest.write_text(page, encoding='utf-8')
        print(f'Wrote {dest}. Local snapshot only; no authentication or refresh service.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 2
if __name__ == '__main__': sys.exit(main())
