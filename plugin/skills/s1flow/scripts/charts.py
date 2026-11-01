"""Render a saved development comparison as one offline HTML page.

    python charts.py comparison.json --out comparison.html

Create the input with `s1flow report TASK --out DIR` (DIR/comparison.json). This renderer
uses only the Python standard library: no model calls, evaluation or rescoring.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import sys
from typing import Any


def read_snapshot(path: Path) -> dict[str, Any]:
    def nonfinite(value: str) -> None:
        raise ValueError(f'non-finite number {value}')

    data = json.loads(path.read_text(encoding='utf-8'), parse_constant=nonfinite)
    if not isinstance(data, dict) or data.get('schema') != 's1flow/comparison@2' or data.get('scope') != 'dev':
        raise ValueError('expected a v2 dev snapshot; regenerate with s1flow report TASK --out DIR')
    if not isinstance(data.get('task'), str) or not isinstance(data.get('objective'), dict):
        raise ValueError('comparison is missing its task or objective')
    rows = data.get('candidates')
    if not isinstance(rows, list) or any(not isinstance(row, dict) or not isinstance(row.get('candidate'), str) for row in rows):
        raise ValueError('comparison candidates must be named objects')
    definitions = data.get('metric_definitions')
    if not isinstance(definitions, list) or any(not isinstance(d, dict) or not isinstance(d.get('key'), str) for d in definitions):
        raise ValueError('comparison is missing metric definitions; regenerate the v2 snapshot')
    metric_keys = [d['key'] for d in definitions]
    if len(metric_keys) != len(set(metric_keys)) or any(not isinstance(row.get('metrics'), dict) or set(row['metrics']) != set(metric_keys) for row in rows):
        raise ValueError('comparison metric definitions and values do not match')
    names = [row['candidate'] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError('comparison has duplicate candidate identifiers')
    ranking = data.get('ranking')
    if ranking is not None and (not isinstance(ranking, list) or any(not isinstance(p, dict) or p.get('candidate') not in names for p in ranking)):
        raise ValueError('comparison ranking names a candidate it does not hold')
    return data


def render(data: dict[str, Any]) -> str:
    template = Path(__file__).with_suffix('.html').read_text(encoding='utf-8')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    # A question may contain HTML or code. It remains inert JSON and is displayed
    # through textContent; it can never close this script element.
    payload = payload.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    payload = payload.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return template.replace('__TITLE__', html.escape(f"{data['task']} · s1flow comparison")).replace('__DATA__', payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('snapshot', type=Path, help='DIR/comparison.json saved by s1flow report TASK --out DIR')
    parser.add_argument('--out', type=Path, help='HTML destination (default: beside the snapshot)')
    args = parser.parse_args(argv)
    out = args.out or args.snapshot.with_suffix('.html')
    if out.resolve() == args.snapshot.resolve():
        parser.error('--out must not overwrite the comparison snapshot')
    try:
        page = render(read_snapshot(args.snapshot))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding='utf-8')
    except (OSError, UnicodeError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
