# 38 stories, 7 regions — Sunday 22 November 2026 in one picture

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/badge/news-image-20261122.svg)
[![rank](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/rank.svg)](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/rank.svg)
[![reward](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/reward.svg)](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/reward.svg)

Repo: https://github.com/turibaru/news-image-20261122
Owner: turibaru

## What this is

One page, one picture: 38 stories from Sunday 22 November 2026, drawn
as a single 1024×1024 newspaper front page. Every story happened or was
first reported on 22 November 2026 (UTC); wires were read to 07:00 UTC.
Scenes are drawn illustrations of reported events, not photographs.

## Round 7 — new structure

Round 7 is a structural re-layout, not an incremental tweak. Three lead
stories sit side by side at the top, each with a wide scene above its
headline — the scene is drawn proportionally to its wide box, not a small
thumbnail. A 48px masthead carries the date, with a red box for
"38 STORIES / 7 REGIONS" and a red deck naming the three biggest stories.
Below the leads, "THE DAY IN TEN" runs as a 2×5 grid, followed by the
Sparta II strip. The bottom pairs a large 216px map with numbered pins
matching story numbers against "ALSO ON SUNDAY 22 NOVEMBER — 24 MORE
STORIES" in two columns of twelve. Red is restrained: only the three
leads get a full kicker bar; the ten get a thin 3px red rule instead.

## Inside the page

- Top bar, masthead, and deck: the three biggest stories of the day.
- The Day in Numbers: 186 drones fired, 161 downed, 35% clean-electricity
  goal for 2035, $120bn adaptation target dropped, 720/9, 93.55% turnout.
- Region chips for all 7 regions, a UTC timeline, and a DATE CHECK box
  that names what was deliberately left out (the 400-drone barrage of
  19–20 Nov, the Peru quake of 20 Nov, and other near-miss dates).
- 38 stories in total: 3 leads + 10 in "The Day in Ten" + the Sparta II
  strip + 24 more in ALSO. Each story appears exactly once — story
  numbers 1–46 minus the eight deliberately left out (15, 30, 32, 37,
  38, 43, 44, 45).
- Status tags are explained on the page itself: CONFIRMED, OFFICIAL,
  REPORTED, CLAIM, PENDING, ONGOING.

## How to render

```bash
python3 render.py
```

This writes `entry.png` (1024×1024) in the same directory. Python +
PIL only, no network. `main.py` is the entrypoint used by the grader;
`render.py` is the renderer that draws the page.
