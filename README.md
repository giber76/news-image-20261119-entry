[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/giber76/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# Thursday 19 November 2026 — one front page

A dense broadsheet that sums up Thursday 19 November 2026's world news
in one image: 50 stories, 6 continents, one front page — the winning genre
of the daily news-image contests.

- **Masthead:** "Thursday 19 November 2026" — 50 stories, 6 continents.
- **3 illustrated hero cards:** GTA VI's global rollout begins; Democrats
  nominate Hakeem Jeffries for Speaker; Iran widens its fire across the Gulf.
- **8 illustrated medium cards:** Nvidia's $115.8bn quarter, Anthropic's
  $81.3bn IPO, the Dow's 561-point slide, Voyager 1 one light-day out,
  Trump–Xi–Putin at APEC, the Gaza ground operation, the Crimea bridge
  hit again, the EU's €45bn Ukraine loan.
- **By the numbers:** 16M, $115.8bn, 561, $81.3bn, 1 light-day.
- **Also on 19 November:** numbered list, stories 12–50.
- **Where it happened:** a dotted world map with 12 numbered pins,
  matching the stories above, plus a timeline of the day in order.

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
