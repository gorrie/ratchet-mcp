"""Mirror an export tree onto a git clone (rsync -a --delete, minus .git). Usage: mirror_sync.py <src> <dst>"""
import os
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
want = {p.relative_to(src) for p in src.rglob("*") if p.is_file()}
have = {p.relative_to(dst) for p in dst.rglob("*") if p.is_file() and ".git" not in p.relative_to(dst).parts}
for rel in sorted(have - want):
    (dst / rel).unlink()
for rel in sorted(want):
    (dst / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / rel, dst / rel)
for d in sorted((p for p in dst.rglob("*") if p.is_dir() and ".git" not in p.relative_to(dst).parts),
                key=lambda p: len(p.parts), reverse=True):
    if not any(d.iterdir()):
        d.rmdir()
print("synced: %d files, %d removed" % (len(want), len(have - want)))
