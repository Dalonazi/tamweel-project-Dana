"""Check local Markdown links; external services are checked separately in a browser."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import re


def check_links(root):
    root = Path(root).resolve()
    failures = []
    count = 0
    for page in root.rglob('*.md'):
        if any(p in {'.git', '.venv', '.check-output', 'evidence'} for p in page.relative_to(root).parts):
            continue
        for link in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', page.read_text(encoding='utf-8-sig')):
            parsed = urlsplit(link.strip('<>'))
            if parsed.scheme or not parsed.path:
                continue
            target = (page.parent/unquote(parsed.path)).resolve()
            count += 1
            if not target.is_relative_to(root) or not target.exists():
                failures.append(f'{page.relative_to(root)} -> {link}')
    return count, failures


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path.cwd())
    args = p.parse_args()
    count, failures = check_links(args.root)
    print(f'Local Markdown links: {count}; broken: {len(failures)}. External links not assessed.')
    print('\n'.join(failures))
    raise SystemExit(bool(failures))
