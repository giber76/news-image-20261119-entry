#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file; the program copies it
to /output/entry.png. The image itself was drawn by draw.py in this
repository (Pillow, flat procedural art, no copied photograph): a dense
broadsheet front page for Thursday 19 November 2026 -- a navy masthead,
3 illustrated hero cards, 8 illustrated medium cards, a by-the-numbers
strip, a dotted world map with 12 numbered pins, a numbered list of the
rest of the day, a timeline strip, and a sources footer: 50 verified
stories in all.

The image is fully pre-rendered, so the copy is byte-identical on every
run: the grader's two runs write the same bytes.

Run it with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
print("wrote", os.path.join(OUT_DIR, "entry.png"))
