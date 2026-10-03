# Crystal Care Guide (Mooncat Crystals)

Free public lookup at care.mooncatcrystals.com: type a crystal, see how to clean it, whether it's water/sun safe, how fragile it is, how to cleanse it, and a shop link. Optional sign-up emails a printable chart (chart.html).

- `crystals.json`: the hand-edited care data (one entry per crystal). See its `_about` for field meanings and tone rules.
- `build.py`: run after editing crystals.json. Writes `data.json` (what the pages load) and `review.html` (fact-check sheet).
- `index.html`: the lookup. `chart.html`: printable chart.
- Email links to the tool should use `?ref=list`: subscribers then see a direct "Open the Printable Chart" button instead of the chart sign-up (no second opt-in).
- `functions/api/care-submit.js`: adds chart sign-ups to the Flodesk segment in `FLODESK_SEGMENT_CARE`.

Look: loads the Crystal Skool dashboard's shared theme (https://dashboard.mooncatcrystals.com/mooncat-theme.css) so colors, fonts and light/dark stay in sync with Crystal Skool. Theme key "crystalskool-theme"; dashboard links pass ?theme=.

Hosting: Cloudflare Pages (no build command, output `/`), env vars `FLODESK_API_KEY` (secret) and `FLODESK_SEGMENT_CARE`.

Care rules: water is only for cleaning off dust, and only for quartz-family stones; cleansing = selenite plate (several hours or overnight), sound, smoke, intention (never moonlight or water). Calm tone; handling tips, never scare copy. Universal note is a light 'Common sense reminder', not a lecture. Lean cautious when sources disagree.
