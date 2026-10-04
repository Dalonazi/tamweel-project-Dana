"""Rebuild the final project inventory after completing your own evidence."""
import argparse
from pathlib import Path
from submission_contract import build_manifest

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--bundle', action='store_true')
    args = p.parse_args()
    result = build_manifest(args.root, args.bundle)
    print(f"MANIFEST_CREATED: {len(result['files'])} files; integrity only, not readiness or a grade.")
