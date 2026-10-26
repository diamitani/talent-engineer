#!/usr/bin/env python3
"""Local failure audit. No network calls, credentials or candidate payloads."""
import argparse
import json
import os
import sys
import time
from pathlib import Path
SYSTEMS = ('workday', 'greenhouse', 'gem', 'brighthire', 'other')
KINDS = ('auth', 'timeout', 'empty', 'mismatch', 'rate_limit', 'other')

def log_path():
    return Path(os.environ.get('TE_FAILURE_LOG', str(Path.home() / '.talent-engineer/failures.jsonl')))

def load(path):
    rows = []
    if not path.exists():
        return rows
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            assert isinstance(row, dict) and row.get('system') in SYSTEMS
            assert row.get('event', 'failure') in ('failure', 'reset')
            assert isinstance(row.get('ts'), (float, int)) and not isinstance(row['ts'], bool)
            assert 0 <= row['ts'] <= time.time() + 300
            assert isinstance(row.get('tool', ''), str) and isinstance(row.get('detail', ''), str)
        except (ValueError, TypeError, AssertionError):
            raise ValueError(f'Invalid audit log row {i}; preserve the file and investigate before continuing.')
        rows.append(row)
    return rows

def append(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row) + '\n')
    try:
        path.chmod(0o600)
    except OSError:
        pass

def states(rows, now):
    result = {}
    for system in SYSTEMS:
        relevant = [r for r in rows if r['system'] == system]
        reset = max((r['ts'] for r in relevant if r.get('event') == 'reset'), default=0)
        failures = [r for r in relevant if r.get('event', 'failure') == 'failure']
        count = sum(0 <= now-r['ts'] <= 86400 and r['ts'] > reset for r in failures)
        result[system] = {'failures_24h_since_reset': count, 'all_time': len(failures),
                          'state': 'STOP' if count >= 3 else ('watch' if count else 'no recorded failures; connection unverified')}
    return result

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    l = sub.add_parser('log')
    l.add_argument('--system', required=True, choices=SYSTEMS)
    l.add_argument('--tool', required=True)
    l.add_argument('--kind', required=True, choices=KINDS)
    l.add_argument('--detail', default='')
    s = sub.add_parser('status'); s.add_argument('--json', action='store_true')
    r = sub.add_parser('recent'); r.add_argument('-n', type=int, default=20)
    c = sub.add_parser('clear', help='Reset active circuit after a confirmed fix; retains history')
    c.add_argument('--system', required=True, choices=SYSTEMS)
    c.add_argument('--reason', required=True)
    args = p.parse_args(argv)
    path = log_path()
    try:
        rows = load(path)
        if args.command == 'log':
            append(path, {'ts': time.time(), 'event': 'failure', 'system': args.system,
                          'tool': args.tool, 'kind': args.kind, 'detail': args.detail})
            print('Failure recorded. Run status before another call.')
        elif args.command == 'clear':
            append(path, {'ts': time.time(), 'event': 'reset', 'system': args.system, 'detail': args.reason})
            print('Active count reset; history retained.')
        elif args.command == 'recent':
            if args.n <= 0: raise ValueError('-n must be positive')
            for row in rows[-args.n:][::-1]: print(json.dumps(row))
        else:
            summary = states(rows, time.time())
            if args.json: print(json.dumps(summary, indent=2))
            else:
                for name, item in summary.items():
                    print(f"{name}: {item['failures_24h_since_reset']} active failures / 24h; {item['all_time']} historical; {item['state']}")
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
