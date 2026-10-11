# Brief: TechNext AI Solution posts (templated series)

Work folder: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ai` (run commands from here).
TEMPLATE (DONE - copy its structure exactly): `v3/p12.html` (RAG Knowledge Assistants), render `qa/p12.jpg`. LOOK first.
Style background: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ind\BRIEF.md` (hero-scene style, kit API, cast rules,
render/QA loop) - read it, everything there applies.

## Owner direction (8 Oct 2026)
"create social media posting, make it more dynamic base on content and information from title and subtitle. make it
like it's templated posting. dont change the position of logo and link of website."
=> A SERIES TEMPLATE. Identical across the 4 posts and NOT to be moved:
- `.sp-logos` logo row, `.sp-foot` URL pill bottom-centre (no inline styles on it).
- `.tp-chip` "AI Solution · <b>Service</b>" (with the Odoo icon), `.tp-h` headline (2 lines, built from the menu title,
  `<em>` accent on the key phrase), `.tp-sub` subline (from the menu subtitle / page lead). Classes in assets/series.css.
- Per post only: the accent colours (`--acc --acc-l --acc-d` in :root) and the SCENE below y ~540 (canvas via SP.draw +
  `#flow` SVG overlay for dynamic lines/particles + soft `.bub` / `.rec` cards + optional Nexi PNG `.nexi-png`).
- "More dynamic": every scene must SHOW the service working as motion: flows, connectors, items travelling, a step
  sequence, glow on the thing that matters - like p12's flying pages and the citation thread. Hero-scene style (soft,
  flat, kit cast), no comic outlines. Nexi (assets/sp/nexi/*.png: hello, present, point-left, point-right, think, wow,
  celebrate, clap, love) is the AI and should appear as the assistant in each.
- Keep faces clear of cards/lines/particles; people on the floor; all record values labelled sample.

## Posts (copy facts from these lines only; pages are in C:\Users\leuss\ClaudeWork\tn-social-ref)
| NN | Service | file / <title> | menu subtitle | page line (for the sub / details) | URL |
|---|---|---|---|---|---|
| 12 | RAG Knowledge Assistants | DONE | Answers grounded in your own documents. | Ask in plain language. Get the answer, with the source. | technext.asia/solutions/ai-knowledge |
| 13 | Odoo + AI integrations | v3/p13.html / odoo-ai-integrations | AI working inside your ERP records. | AI that works inside Odoo, on your data. Vendor bills read and matched, customer replies drafted, questions answered from your own records. A person approves every step. | technext.asia/odoo/ai-integration |
| 14 | Workflow Automation | v3/p14.html / ai-workflow-automation | Agents that run multi-step tasks. | Let an agent do the steps. Keep the decision. Classify the email, pull the record, prepare the document, route it, follow up; a person approves anything irreversible. Agents prepare; people post. | technext.asia/solutions/ai-automation |
| 15 | AI Chatbots | v3/p15.html / ai-chatbots | Web, WhatsApp and in-app assistants. | A chatbot that knows your business and knows when to hand over. Answers from your content, looks up orders, bookings and invoices, qualifies leads, hands over to a person with full context. | technext.asia/solutions/ai-chatbots |

Chip icons: knowledge.svg (12), ai_app.svg (13), mail.svg or project.svg (14), im_livechat.svg or whatsapp.svg (15).

## Render
`python C:\Users\leuss\.claude\skills\technext-site-posts\scripts\render.py v3/pNN.html --out qa --force --port <yours>`
then a jpg + Read it. Done = ALL CLEAN without --force AND it looks right. Report: file, QA line, one paragraph on the
scene. Don't touch p12 or other posts, don't deliver.
