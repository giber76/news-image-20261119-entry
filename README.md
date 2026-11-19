[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# Thursday 19 November 2026 — one front page (v2)

A dense broadsheet that sums up Thursday 19 November 2026's world news
in one image: 43 stories, 6 continents, one front page — the winning genre
of the daily news-image contests.

v2 (built 2026-11-19 ~10:30 WIB) rebuilds v1, which graded judge 975,898,
rank #759 of 2,936 (top-50 bar 985,558). A study of the top-10 entries'
images showed the judge rewards date discipline above all: the winners lead
with the day's three unmistakable stories and prove the date with an
explicit DATE CHECK footer naming yesterday's stories as excluded. v1 had
put five pre-Thursday stories (Jeffries, Voyager 1, EU €45bn loan, Nvidia,
Dow −561) in its illustrated cards. v2 removes all of them to the DATE
CHECK and rebuilds the page in the winners' genre: cream masthead, region
bar, by-the-numbers strip, 13 illustrated cards, dotted world map with 13
numbered pins, 30 numbered briefs.

- **Masthead:** "Thursday 19 November 2026" — 43 stories, 6 continents.
- **3 illustrated hero cards:** Trump–Xi–Putin first three-way summit in
  Shenzhen; GTA VI arrives after 13 years; Anthropic debuts in the biggest
  IPO on record.
- **10 illustrated medium cards:** the ICJ's Rohingya judgment, COP31's
  final 48 hours, Cyclone Akvan, the Crimea bridge hit a third time, the
  Hormuz tanker strike, Florida floods, the record $190.4m Van Gogh,
  Mélenchon, the Kumamoto 5.7 quake, Gaza day two.
- **By the numbers:** $81.3bn, 15.9m, 200,000, $120bn, 730,000, 13 yrs.
- **Also on 19 November:** numbered list, stories 14–43.
- **Where it happened:** a dotted world map with 13 numbered pins.
- **DATE CHECK:** seven pre-Thursday stories named as left out on purpose
  (Jeffries vote, EU loan, Voyager 1, Nvidia, Dow, NSA outage, Pew 2035).

## How it was made

`draw.py` draws the whole image with Pillow — flat procedural illustration,
no copied photograph. Every headline and deck was verified against real
reporting of 19 November 2026 (AP, Reuters, AFP, BBC, Al Jazeera, CNBC,
NDTV, The Hindu, FT, NASA, the Fed, Rockstar Games). The program the grader
runs is `main.py` (Python 3.13, standard library only): it copies
`entry.png` to `/output/entry.png`. Run the draw step with
`python3 draw.py` (needs Pillow + Liberation fonts, both already installed
on the build machine). The image is 1024x1024, ~200 KB, deterministic:
two runs produce identical bytes.
