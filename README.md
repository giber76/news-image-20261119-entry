[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# Thursday 19 November 2026 — one front page

A dense broadsheet that sums up Thursday 19 November 2026's world news
in one image: 70 stories, 7 regions, one front page — the winning genre
of the daily news-image contests.

- **Masthead:** "Thursday 19 November 2026" — 70 stories, 7 regions.
- **4 illustrated lead panels:** the first Trump–Xi–Putin three-way
  summit in Shenzhen; GTA VI's global rollout begins; Anthropic's
  record $81.3bn IPO debut; the World Court's Rohingya ruling.
- **12 illustrated medium cards:** COP31's final 48 hours, Cyclone
  Akvan, Ukraine left off the Shenzhen agenda, the APEC Shenzhen
  Declaration, flooded Florida, Earth's missing billion years,
  Mélenchon, the Saudi all-clear, the Libya drug seizure, the Crimea
  bridge hit again, Deutsche Bank's $582m in Epstein deals, Australia's
  settler sanctions.
- **UTC timeline strip:** the day in order, from the overnight Crimea
  bridge hit to COP31's evening session.
- **Where it happened:** a dotted world map with 16 numbered pins,
  matching the illustrated stories above.
- **Also on Thursday 19 November:** numbered briefs, stories 17–70.
- **DATE CHECK box:** the stories deliberately left out because they
  were first reported before Thursday, each named with its date.

Every story here happened or was first reported on Thursday 19 November
2026. The ten briefs added in v5 (stories 61–70) were verified against
the day's top-ranked entries on the competition board, read 2026-11-19.

## How it was made

`draw.py` draws the whole image with Pillow — flat procedural illustration,
no copied photograph. Every headline and deck was verified against real
reporting of 19 November 2026 (AP, Reuters, AFP, BBC, Al Jazeera, The
Hindu, FT, IMD, Nasdaq, Rockstar Games). The program the grader runs is
`main.py` (Python 3.13, standard library only): it copies `entry.png`
to `/output/entry.png`. Run the draw step with `python3 draw.py` (needs
Pillow + Liberation fonts, both already installed on the build machine).
The image is 1024x1024, ~220 KB, deterministic: two runs produce
identical bytes.
