# Brief: TechNext pain-point scenario posts (templated split scenes)

Work folder: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-pain` (run commands from here).
TEMPLATE (DONE - copy its structure exactly): `v3/p20.html` (Month-end close), render `qa/20-technext-pain-month-end-close.png`. LOOK first.
Also read, everything applies: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ai\BRIEF.md` (templated frame) and
`C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ind\BRIEF.md` (hero-scene style, kit API, cast, render loop).

## Owner direction
"create a scenario, painpoints. atleast 5 social media posting". Each post = one everyday business pain told as a
scenario, split "TODAY" (the pain: muted/greyish, clutter, stressed person: mood 'wow', hands on head, sweat drops)
vs "WITH ODOO" (the fix: bright, calm, mood 'happy', one clean flow). Same person on both sides.
- Fixed frame (assets/series.css + assets/pain.css): logo row and URL pill bottom-centre untouched; `.tp-chip pain`
  "Pain point · <b>Topic</b>" (+ Odoo icon), `.tp-h` = the pain as a question, 2 lines, force the break with `<br>` so
  the pain words in `<span class="pain">` sit together on line 2; `.tp-sub` = "<the symptom>. <b>The Odoo fix.</b>"
  (one line). `.lab.today` / `.lab.fix` labels at the same spots as p20, `.vs` badge on the seam, one `.note.bad`
  bottom-left and one `.note.good` bottom-right (sample values). Only accent vars + the two half-scenes change.
- Make each half dynamic (flows, things flying/clashing on the left, one clean connected flow on the right).
- Cast: SEA/East-Asian, dark straight hair, business-casual for client staff; no wheelchairs; monitors beside faces.
- OVERFLOW RULE: render.py fails on text overflow; also check by eye that no drawing crosses any text, faces clear.
- No invented statistics or promises: the "Today" numbers are a scenario (label sample); the fix describes what the
  Odoo feature does, not a guaranteed result.

| NN | Topic (chip) | file / <title> | headline (pain question) | sub (symptom. **fix**) | Odoo icon | URL | accent |
|---|---|---|---|---|---|---|---|
| 20 | Month-end close | DONE | Month-end still takes / two weeks? | | accountant | technext.asia/odoo/apps/accounting | green |
| 21 | Stock mismatch | v3/p21.html / pain-stock-mismatch | The system says 20. / The shelf says zero. | Counts drift between the store and the books. **Odoo updates stock on every sale.** | stock.svg | technext.asia/odoo/apps/inventory | orange #E07B28 |
| 22 | Re-typing orders | v3/p22.html / pain-retyping-orders | Typing the same order / three times? | Sales, warehouse and invoicing in separate files. **One Odoo record runs quote to cash.** | sale.svg | technext.asia/solutions/odoo-erp | blue #3167CA |
| 23 | Approvals in chat | v3/p23.html / pain-approvals-in-chat | Approvals buried in / group chats? | Purchase requests lost in WhatsApp threads. **Odoo Approvals routes and logs each one.** | approvals.svg | technext.asia/odoo/apps/approvals | teal #14A38B |
| 24 | Finding documents | v3/p24.html / pain-finding-documents | Which file is / the latest version? | Policies in ten folders and three inboxes. **Ask the knowledge assistant, get the source.** | knowledge.svg | technext.asia/solutions/ai-knowledge | purple #6B4FA0 |
| 25 | Lost leads | v3/p25.html / pain-lost-leads | Leads slipping through / five inboxes? | Web forms, emails and chats with no owner. **Odoo CRM gives every lead a stage and an owner.** | crm.svg | technext.asia/odoo/crm-development | magenta #C2357F |

If a headline/sub wraps badly or overflows, shorten the wording minimally (keep the meaning) and say so in the report.
Render: `python C:\Users\leuss\.claude\skills\technext-site-posts\scripts\render.py v3/pNN.html --out qa --force --port <yours>`,
jpg + Read. Done = ALL CLEAN without --force AND looks right. Report: files, QA line, one paragraph per post.
Don't touch p20 or other posts; don't deliver.
