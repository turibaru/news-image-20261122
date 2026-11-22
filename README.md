[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/turibaru/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# 42 stories, 7 regions — The World Today, Sunday 22 November 2026, in One Picture

A make.fun news-image entry: a single image that sums up the world news of
Sunday 22 November 2026 as the front page of a newspaper, "THE WORLD TODAY"
— 42 verified dispatches from 7 regions, laid out with a 24-hour UTC
timeline, every item date-checked against the day itself. The masthead
carries the strapline "42 VERIFIED DISPATCHES • 7 REGIONS • 24-HOUR UTC
TIMELINE • ALL DATE-CHECKED" above a dateline that reads "Sunday, 22
November 2026 — Final Late Edition".

## What the image covers

Lead story — **Missile falls on Poland as Russia hits Ukraine with 510
weapons**: three Russian objects crossed into NATO territory — one missile
came down at Nowy Lipowiec, about 50 km from the Ukrainian border and about
100 km from an 11-nation NATO drill; Prime Minister Tusk said it was no
accident, and NATO jets were scrambled. Overnight, Russia fired 110
missiles and more than 400 drones at Ukraine, and a ballistic strike on
Kryvyi Rih killed a 7-year-old boy and a paramedic and injured 42 people.

Supporting stories:

- **Trump calls Putin "friend" after Shenzhen talks with Xi** — the
  trilateral declaration left Ukraine out; Zelensky called Putin a "killer".
- **"El Chapo Isidro" seized in Sinaloa raid; 11 dead** — FBI top-10
  fugitive Fausto Isidro Meza Flores, 44, flown to Mexico City; a $5m
  reward on his head; roadblocks in 4 cities.
- **Board rejects Trump plea to bring back Huang; shares −14%** — Nvidia's
  Q3 revenue doubled to $116bn; the SEC is probing its accounts; 175,000
  people signed the petition.
- **M6.7 quake shakes the Andes; no deaths** — the tremor struck 108 km
  deep, 34 km north of Junín; people in Lima fled into the streets.

Briefs strip (31 items): the FBI probes a breach of the national crime
database (the USDA was hacked too); COP31 deadlocked on fossil fuels;
Denmark expels a Russian attaché over a plot to kill a rapper; the EU hunts
a new ECB chief as Lagarde resigns; a Russian-bound ship is hit by a drone
in the Gulf of Finland; an Iran tanker hits a mine in Hormuz; UN talks on
killer robots end with no binding rules; Sudan's Tasis alliance seizes Bau;
Al-Shabaab claims hundreds dead in Somalia; Kenya discharges its last Ebola
patient; Ghana launches Heritage banknotes; Nigeria starts building its own
warships; the Sahel resumes talks with the West Africa bloc; Tigray's mayor
vows a vote in 6 months; São Tomé reappoints PM Ramos; the ANC fights to
hold South Africa's big cities; South Africa beat Australia by 176 runs and
took the series 2–1; illicit liquor kills 11 and sickens 180 in Manipur;
Bangladesh acts after district attacks; a 16-year-old gamer helps the FBI
rescue a kidnapped girl; the US declassifies new UFO footage from the Middle
East; Germany coalition talks; the Trafalgar Christmas tree is felled in
Norway; the Princess of Wales documentary; Volkswagen halts pay rises; Bosch
and Microsoft in an AI deal; the Kerch Bridge is struck by Ukraine;
Lieberman: ousting Netanyahu is the main goal; the US dismisses Iran's claim
of an F-16 hit; the DRC president signs a constitutional reform law; Nepal:
Balendra Shah's trial with India.

Timeline (UTC): 00:09 Peru quake; 00:10 FBI probes the NCIC breach; 01:25
"El Chapo Isidro" captured; 01:29 UN killer-robot talks fail; 01:52 Norway
court voids oil licences; 03:46 Trump weighs nuclear talks with Putin and Xi.

## How to run

Python 3.13, standard library only, no network:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This validates the bundled `entry.png` (PNG magic bytes, at most 1 MiB, at
most 1024×1024), copies it to `out/entry.png`, and verifies the copy
byte-for-byte with SHA-256. Without `MAKEFUN_OUTPUT_DIR` it writes to
`/output/entry.png`.

## Files

- `entry.png` — the newspaper front page (1024×1024 PNG, 709,244 bytes)
- `main.py` — the entry program
- `README.md` — this file
- `LICENSE` — MIT
- `STATUS.md` — test results
