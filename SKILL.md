---
name: technext-site-posts
description: Design TechNext social media image posts (3:4, 2160x2880 PNG, images only, no video), one per technext.asia service (mega menu - ERP, AI Solution, Marketing, Technology), using the website's page designs only as REFERENCE - each post is an original, dynamic illustrated poster built around its own concept (perspective music staff, bird's-eye relay track, isometric group tower...), in the TechNext brand fonts and colours. Use when the user asks for social posts per website service/category/menu item, "posts based on the website design", site-style posts, or the next category in this series (e.g. "now do AI Solution").
---

# TechNext site-inspired posts

**Owner direction (8 Oct 2026):**
1. "make the design more dynamic, no video. image only."
2. "the theme are still similar ... create a design base on the context ... for fonts, still use the technext branding.
   make it more dynamic, dont totaly copy, just use as reference ... make it more unique. dont directly copy."

3. Industries, 8 Oct 2026: "dont use too much comical style. focus on similar style that we currently using to build hero
   section in all pages." => industry posts use the HERO-SCENE style (below), not the outlined comic style.
4. "fix the positioning of logo" (reference images): logos 72px from the sides, row centred ~100px from the top,
   TechNext 47px tall, Odoo 43px; footer 56px from the bottom with 72px side padding; content starts below y 170
   (render.py enforces it). All in kit/brand.css.

5. "always check the overflow text." (8 Oct 2026) => render.py fails on ANY text overflow: HTML/SVG text spilling out
   of its visible box (card, pill, chip) or the frame, text clipped by its box, and canvas text (fillText is hooked)
   cut by the frame, hidden under a card, or colliding with other canvas text. Never ship with --force; read the
   OVERFLOW line, fix the layout (move the card, shorten the label, enlarge the sign), re-render.

So: study the service page (its metaphor, claims, palette, the ink-outline + hard-lip craft), then design a NEW poster.
Never screenshot the site, never paste its cards or scenes. The first attempt (v1, captures of the page heroes) was
rejected for exactly that; `scripts/capture.py` / `make_post.py` stay only for studying a page (grab its copy and a
reference picture), not for output.

## Series map
| # | Category | Service | Page (CTA) | Concept used |
|---|---|---|---|---|
| 01 | ERP | Odoo ERP Implementation | /solutions/odoo-erp | "Every app. One score." perspective staff, Odoo app icons as notes, Nexi conducts, go-live ticket |
| 02 | ERP | CRM Development | /odoo/crm-development | "Pass the lead. Win the deal." bird's-eye track, lead cards racing New > Qualified > Proposition > Won, Won card = quotation |
| 03 | ERP | Enterprise Solution | /solutions/enterprise | "Four companies. One set of numbers." isometric tower, one floor per company, lettering in the iso planes, currency coins to a Group P&L board |
| 04-11 | Industries | Medical, Travel, Retail, Ecommerce, Construction, F&B, Manufacturing, Health & Wellness | /industries/<key> | hero-scene style, one front-on room each (examples/2026-10-08-industries, BRIEF.md) |
| 12-15 | AI Solution | RAG Knowledge Assistants, Odoo + AI integrations, Workflow Automation, AI Chatbots | /solutions/ai-knowledge, /odoo/ai-integration, /solutions/ai-automation, /solutions/ai-chatbots | TEMPLATED series (kit/series.css): reading room + citation thread / invoice into AI-filled bill + Confirm / email along a step track to an approval gate / 3 channels converge on Nexi + hand-over (examples/2026-10-08-ai-template) |
| 16-19 | Company | About TechNext, Careers, Blog, Employee Hub | /company, /careers, /blog, /employee-hub | templated frame, "fresh new environment" each: team lounge with 3 city windows / Taguig plaza recruitment day / café reading corner with article cards / lobby first-day ID printing (examples/2026-10-08-company). Company cast: Asian, semi-casual, EVERY TechNext person incl. new hires wears the blue ID; visitors/candidates grey |
| - | Marketing | Web Design & Development, Social Media Management, Graphic & Brand Assets | /solutions/website, /solutions/social-media, /solutions/brand-assets | |
| - | Technology | IoT Solutions, App Development, Networks | /solutions/iot, /solutions/app-development, /solutions/networks | |
| 90-92 | Nexi intro (2026-10-10) | Say hi to Nexi / Four practices, one guide / Ask Nexi anything Odoo | /nexi, /nexi-explains | site craft on the social-posts brand frame + living brand skins: Nexi's TechNext staff ID (light), four practice playing cards fanned over Nexi (dark), Ask Nexi phone chat (light); one headline treatment each (slab, swash, marker). Pages: technext-social-posts kit/examples/2026-10-10-nexi-intro-87-92/brand |
Confirm hrefs in the built index.html (menu targets move). Number on from the last row.

## Brand (fixed) vs design (free)
- Fixed: Plus Jakarta Sans 800 headlines, Inter body, Caveat hand kicker/notes; TechNext blue #3167CA, ink #1F1F3D, Odoo
  plum #714B67; TechNext logo top-left, plain Odoo wordmark top-right, URL pill at the bottom; ink outline + hard lip
  (3px border, 5-8px offset shadow) as the shared craft. All in `kit/brand.css`.
- Free, and must differ post to post: concept/metaphor, camera (perspective, bird's-eye, isometric, low angle, dutch),
  palette (take the service's world colours), headline treatment (underline swash, highlight slab, marker, outline),
  where the type sits, the props. Check the series map - never reuse a concept or composition.
- Dynamic = depth and direction: converging/curving lines, objects scaled by distance, things crossing the frame edge,
  tilted cards, motion streaks. Not dark sci-fi, not glow, not 3D renders.

## Content
- Claims only from the page / brand guide (Odoo Partner; 10+ countries; SG HQ + PH + VN teams; 11+ enterprise clients).
- Real Odoo vocabulary (default CRM stages, app names, official icons in the site's `assets/img/odoo/*.svg`).
- Sample names/numbers say "sample". Staff, if drawn: Asian, semi-casual, TechNext ID lanyard. Nexi (kit/assets/nexi)
  in about 1 of 3 posts. Her attitude and reaction come from the skill `nexi-character` (offended by the mess, never by the
  person; 46 reactions + 30 variants, a different one per post): a pain post = a rage-ladder / trouble reaction at the mess
  prop, a result post = a win, a "here's how" post = `idea` or `determined`. Render it from the renderer bench
  `films/nx3vsheet.js` / `nx3sheet.js` at the peak time (rembg cut-out) rather than redrawing her face.

## Pipeline
1. Work folder `~/ClaudeWork/site-posts-<date>-<cat>/`; `python <skill>/scripts/setup.py .` (copies site css/img for the
   Odoo icons + kit). Then copy `kit/brand.css` to `assets/brand.css`, `kit/assets/*` to `assets/sp/` (nexi/ included).
   Site source for reference: detached worktree `~/ClaudeWork/tn-social-ref` (refresh from origin/master), preview
   `technext-social-ref` port 4011.
2. Read each service page (text + one look at its hero) and write a concept per post: headline (5-7 words, two beats),
   metaphor, camera, palette, 2-3 props that carry real Odoo detail, where Nexi/notes go. Make the three+ differ.
3. Build `v2/pNN.html` by hand: brand.css + a per-post `<style>`, geometry generated with a small inline script into an
   SVG (see `examples/2026-10-08-erp-v2/` - staff curves, arc lanes, iso() projection, CSS matrix text on iso faces).
   `<title>` = slug. Mark every text block `data-qa="name"`, decorative SVG `data-qa-skip`.
   Script gotcha: never name a global `top`/`name`/`status` (window props) - the whole drawing silently fails.
4. `python <skill>/scripts/render.py v2/pNN.html --out qa/v2 --force` -> look -> fix -> repeat until ALL CLEAN without
   --force (fonts loaded, blocks in frame and not overlapping, all text >= 15 px). Contact-sheet the batch and compare.
   THEN the deep audit (blocking, owner 2026-10-10): `python ~/.claude/skills/technext-social-posts/scripts/audit.py v2/pNN.html --f 34 --port 9495`
   (it understands site pages: `.f` frame). 0 errors required: on-screen text size after zoom/transforms, contrast against
   the real pixels, text covered by the URL pill/cards/art, collisions, text off its plate, canvas text. Decoration only:
   `data-qa-skip`.
5. Render finals to `out-v2/`, captions (`captions.md`, FB/IG/LinkedIn per post), deliver to
   `G:\Shared drives\Marketing\00. TechNext Folder\02. TechNext Social Media Posting Image\<NN>. Site Posts - <Category> (<date>)\Image Posts\`
   (md5 check; a redo overwrites, no duplicates), SendUserFile. Never post or schedule.
6. Add the batch to the series map and any new owner rule above.

## Two styles in this series
- **Poster style** (ERP 01-03, examples/2026-10-08-erp-v2): hand-built SVG concepts, ink outline + lip, Caveat notes.
- **Hero-scene style** (Industries 04-11, examples/2026-10-08-industries): soft flat rooms drawn with the site's own kit
  (`assets/js/industry-world.js` -> IXW.kit: room, person/pill-flat cast, plaque, window, plant) via `kit/scene-post.js`
  (`SP.draw(function (g, K, H) {...})`, H.who/H.person/H.pool/H.blur/H.vignette) + `kit/scene.css` (soft white card,
  soft `.rec` Odoo record cards, `.sp-url.soft`). No outlines, no lips, no stickers. Camera: `K.room(g,1080,1440,k,sx,sy,R)`
  then `g.translate(sx,sy); g.scale(k,k)`; set units, floor y 470; k 1.35-1.6. Front-on rooms read best - a one-point
  perspective corridor was tried and looked wrong. Vary card position (top-left/top-right/bottom/full-width), palette and
  framing per post. Cast: SEA/East-Asian, no wheelchairs; staff in uniform. BRIEF.md is the hand-off brief that let
  three helpers build six posts in parallel (one render port each) - reuse it for the next batch.

## Templated series (AI Solution onward, owner 8 Oct 2026)
"make it more dynamic base on content and information from title and subtitle. make it like it's templated posting.
dont change the position of logo and link of website." => one frame for every post of a category (kit/series.css):
logo row + URL pill bottom-centre untouched, `.tp-chip` "Category · Service", `.tp-h` headline from the menu title
(2 lines, `<em>` accent), `.tp-sub` from the subtitle/page lead. Per post only: accent vars and the scene below y ~540,
which must show the service working as motion (flows, travelling items, step tracks, glow) in the hero-scene style,
with Nexi as the AI. Template + brief: examples/2026-10-08-ai-template (p12 + BRIEF.md). Use the same template for
Marketing and Technology unless the owner says otherwise.

## Pain-point scenario series (posts 20-25, 8 Oct 2026)
"create a scenario, painpoints. atleast 5 social media posting" => kit/pain.css on top of series.css: chip "Pain point ·
Topic", headline = the pain as a question (pain words in `<span class="pain">`, forced onto line 2), sub = "symptom.
**fix.**" on ONE line (shorten wording if it wraps), split scene with a tilted seam: TODAY (muted, clutter, same person
stressed: mood wow, hands on head, sweat) vs WITH ODOO (bright, one clean flow), .lab/.vs/.note at fixed spots.
Scenario numbers are labelled sample; the fix describes the feature, never a promised result. Done: month-end close,
stock mismatch, re-typing orders, approvals in chat, finding documents, lost leads (examples/2026-10-08-pain-points).
