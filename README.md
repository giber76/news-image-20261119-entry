[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# Thursday 19 November 2026 — one front page (v4)

A dense broadsheet that sums up Thursday 19 November 2026's world news
in one image: 60 stories, 7 regions, one front page — the structure that
won the 17 November final (50 sourced stories, a UTC timeline, four large
lead panels, twelve medium cards, a numbered-pin map, briefs to 50, and
an explicit DATE CHECK).

v4 (built 2026-11-19 ~13:45 WIB) fixes a real defect Giber caught in v3:
the Florida flood houses drew above their card and covered lead #4's
(World Court) deck — "genocide" printed as "...cide ruling". Every
picture is now rendered onto its own layer and pasted, so no picture can
draw outside its box, and the medium pictures' unscaled sizes are scaled
to fit. v4 also adds ten more verified Thursday stories as briefs,
taking the total from 50 to 60.

v3 (built 2026-11-19 ~13:00 WIB) rebuilds v2, which Giber saw but did not
approve for submit. v1 graded judge 975,839, rank #1,125 of 4,363
(top-50 bar 986,994). Two winner studies drive v3: the 19 November dev
board top 4, and the 17 November FINAL winners (icantcodefyi 849,510 and
gabrieldo 837,047 — the same image twice — plus cendana-utara 812,994).
v3 swaps v2's five weak cards (Van Gogh, sale Wed evening; Gaza day-two,
ground op began Wed; Kumamoto quake, in no winner's cards; Crimea bridge
and Hormuz tanker, absent from every winner's top 13) for the winners'
consensus cards, and adopts the final-winning skeleton: a UTC timeline
strip, FOUR large illustrated leads (the ICJ Rohingya ruling joins the
summit, GTA VI and the Anthropic IPO), twelve medium cards, and briefs
to 60 stories.

- **Masthead:** "Thursday 19 November 2026" — 60 stories, 7 regions,
  every one from this Thursday.
- **The day in UTC:** six slots mapping the day's arc — Crimea bridge
  overnight, Akvan's evacuation at ~06:00 UTC, the Rohingya judgment at
  09:00 UTC, Anthropic trading at ~14:30 UTC, the Shenzhen Declaration
  by day, COP31 working into the evening.
- **4 illustrated lead panels:** Trump–Xi–Putin first three-way summit
  in Shenzhen; GTA VI arrives after 13 years; Anthropic debuts in the
  biggest IPO on record; the World Court rules on Myanmar's Rohingya
  case. Each carries a CONFIRMED label and its source.
- **12 illustrated medium cards:** COP31's final 48 hours, Cyclone
  Akvan, Ukraine watching Shenzhen, the APEC Shenzhen Declaration,
  Florida floods, Earth's missing billion years, Mélenchon, the Saudi
  all-clear, the Libya drug seizure, the Crimea bridge hit, Deutsche
  Bank's $582m in Epstein deals, Australia's settler sanctions.
- **Where it happened:** a dotted world map with 16 numbered pins,
  colour-coded by region, with a legend.
- **Also on 19 November:** numbered briefs, stories 17–60.
- **DATE CHECK:** ten pre-Thursday stories named as left out on purpose
  with their dates (Jeffries vote, EU loan, Voyager 1, Nvidia, Dow, NSA
  outage, Pew 2035, Van Gogh sale, Gaza ground op, Anthropic's $83
  price).

## How it was made

`draw.py` draws the whole image with Pillow — flat procedural illustration,
no copied photograph, no copied winner art. Every headline and deck was
verified against real reporting of 19 November 2026 (AP, Reuters, AFP,
BBC, Al Jazeera, The Hindu, FT, IMD, Nasdaq, Rockstar Games) and
cross-checked against the day's top entries. The program the grader runs
is `main.py` (Python 3.13, standard library only): it copies `entry.png`
to `/output/entry.png`. Run the draw step with `python3 draw.py` (needs
Pillow + Liberation fonts, both already installed on the build machine).
The image is 1024x1024, ~219 KB, deterministic: two runs produce
identical bytes.
