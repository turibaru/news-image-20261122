# 38 stories, 7 regions — Sunday 22 November 2026 in one picture

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/badge/news-image-20261122.svg)
[![rank](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/rank.svg)](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/rank.svg)
[![reward](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/reward.svg)](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/reward.svg)

Owner: [turibaru](https://github.com/turibaru/news-image-20261122)

Repo: https://github.com/turibaru/news-image-20261122

## What this is

One page, 1024×1024, that tells the whole of Sunday 22 November 2026 in
one picture: **38 stories from 7 regions**, every story dated to that day
(UTC) and checked against the wires read to 07:00 UTC.

## R7-fix — what changed

This is the R7-fix revision of the R7 structure. One fix only:

- **Masthead raksasa 64px, satu baris.** "Sunday 22 November 2026" in
  DejaVu Serif Bold 64px, navy, at (10, 28) — the date itself is the
  masthead, the way the top entries do it. Measured width 963px, so the
  line runs x 10..973 inside the 1004px content width with 41px to
  spare. The red box is gone from the masthead band.
- **The red box moved to the top bar.** The top bar (right) now carries
  the count: "38 STORIES · 7 REGIONS · ONE DAY — ONE PICTURE". The old
  top-bar text ("SUNDAY 22 NOVEMBER 2026 · ONE PAGE") is removed — it
  duplicated the giant date below it. Vertical cost of the fix: zero;
  the masthead block stays 88px.


## Structure (R7, unchanged apart from the fix above)

- **Top bar (24px, navy):** "THE WORLD IN ONE DAY" left; the
  "38 STORIES · 7 REGIONS · ONE DAY — ONE PICTURE" count right.
- **Masthead (88px):** giant 64px date, one line, plus a red serif deck
  of the three biggest stories of the day.
- **The day in numbers (62px):** 186 drones fired at Ukraine overnight,
  161 downed or jammed, 35% clean-electricity goal for 2035, $120bn
  adaptation target dropped, 720/9 India's record Test total in NZ,
  93.55% Hong Kong turnout.
- **Region bar + UTC strip:** 7 region chips (Europe 9, Middle East 4,
  Asia-Pacific 7, Americas 5, Africa 8, Oceania 2, World 3) and the day
  in UTC, 01:00–06:00.
- **3 leads side by side (200px each):** Russia's 186-drone night over
  Ukraine; COP31's final text with no mention of fossil fuels; Iran's
  radar-strike claim vs Bahrain's denial. Each lead has a red kicker bar
  with its status pill, a wide scene drawn above the headline, and its
  source line. Red restraint: kicker bars appear only on the leads.
- **The day in ten (254px):** 2 rows × 5 cards, each with a thin red
  rule (not a kicker bar), a scene strip, region label, headline, body,
  and status + source.
- **Card 35 (54px strip):** "Russian cargo ship Sparta II still
  burning" — headline + "CONFIRMED · Reuters" only, no invented body.
- **Bottom (216px):** a 330×216 world map with numbered pins matching
  the story numbers, next to ALSO — 24 more stories in 2 columns of 12,
  each with its number, headline, status, and source where there is one.
- **Legend, DATE CHECK, footer:** how to read the tags; the DATE CHECK
  box listing what was deliberately left out (the 400-drone barrage of
  19–20 Nov, the Peru quake of 20 Nov, the 'El Chapo Isidro' arrest of
  21 Nov, the Shenzhen summit of 19 Nov, the Poland missiles of 20 Nov);
  sources and the note that scenes are drawn illustrations of reported
  events, not photographs.

Total height is exactly 1024px: 24 + 88 + 62 + 20 + 16 + 200 + 18 + 254
+ 54 + 216 + 9 + 34 + 17 + 12. Story count is exactly 38 — 3 leads +
10 in "the day in ten" + 1 strip card (35) + 24 in ALSO — each story
numbered 1–46 exactly once, minus the eight deliberately dropped
(15, 30, 32, 37, 38, 43, 44, 45).

## How to render

```sh
python3 render.py
```

This writes `entry.png` (1024×1024) next to `render.py`. Python + PIL
only, no network, no extra dependencies. `main.py` is unchanged.
