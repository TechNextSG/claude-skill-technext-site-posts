# Brief: TechNext Company posts (templated series, fresh environments)

Work folder: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-company` (run commands from here).
TEMPLATE (DONE, copy its structure): `v3/p16.html` (About TechNext), render `qa/16-technext-about-technext.png` - LOOK first.
Also read, everything applies: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ai\BRIEF.md` (templated frame rules)
and `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ind\BRIEF.md` (hero-scene style, kit API, render loop).

## Owner direction
"create fresh new environment" for the Company menu (About TechNext, Careers, Blog, Employee Hub), social posts.
- Same templated frame as the AI series: logo row + URL pill bottom-centre untouched; `.tp-chip` "Company · <b>X</b>",
  `.tp-h` headline, `.tp-sub` subline (classes in assets/series.css). Only accent vars + the scene change.
- FRESH environment = a new place we have not drawn before (not the website's company-page scenes: no newsroom desk,
  no "201 room", no office replicas). Make it dynamic (things travelling, glow, flows, depth), hero-scene style
  (soft flat, kit cast), no comic outlines.
- COMPANY CAST RULES (owner): TechNext people are all Asian (SEA / East-Asian skin, straight dark hair), semi-casual
  clothes (outfit 'polo', 'tee', 'hoodie', cardigan-like 'blazer' in soft colours; no suits/uniforms), and EVERY TechNext
  person wears the TechNext ID: `idcard: '#3167CA'`. Visitors / candidates wear a grey pass: `idcard: '#9AA6BC'`.
  No deep skin tones or curly hair, no wheelchairs. Monitors beside seated people, never in front of faces.
- OVERFLOW RULE (owner): "always check the overflow text" - render.py now fails on text spilling out of its box,
  clipped, cut by the frame, or canvas text hidden under a card / colliding. Also check by eye that no decorative SVG
  line or icon crosses any text (the checker can't see those).
- Facts only from these lines (pages in C:\Users\leuss\ClaudeWork\tn-social-ref). Names/figures in scenes = sample.

| NN | Item | file / <title> | menu subtitle | page facts | URL | chip icon |
|---|---|---|---|---|---|---|
| 16 | About TechNext | DONE | Who we are, how we work, where to find us. | | technext.asia/company | logo-plane.png |
| 17 | Careers | v3/p17.html / careers | Recruitment day: open roles in Taguig City. | "Build the systems companies run on." Hiring in Taguig City, Metro Manila: Odoo architects and consultants, finance, HR, sales and marketing. Six open roles. Taguig is the main development and consulting hub; work with Singapore HQ and AI engineers in Ho Chi Minh City on Odoo projects for clients in 10+ countries. Recruitment for developers and consultants, plus full-cycle hiring for other roles. | technext.asia/careers | odoo/hr_recruitment.svg |
| 18 | Blog | v3/p18.html / blog | Odoo 20 news and plain-language ERP guides. | "Odoo 20 is here. We explain it." What changes in each Odoo release, what it means for companies in Singapore, the Philippines and Vietnam, how ERP projects actually run. Written by the TechNext team. Article titles: "Odoo 20: what's new, in plain language"; "How an Odoo implementation works, step by step"; "InvoiceNow for GST-registered businesses: the dates, and what to do now"; "Odoo 20 in Singapore, the Philippines and Vietnam: the country changes". | technext.asia/blog | odoo/website_blog.svg |
| 19 | Employee Hub | v3/p19.html / employee-hub | Employee sheets and the TechNext 201. | "Every TechNext person, on file." One employee information sheet for each person, the TechNext ID we all wear, three offices: Singapore, Taguig City, Ho Chi Minh City. | technext.asia/employee-hub | odoo/hr.svg |

Render: `python C:\Users\leuss\.claude\skills\technext-site-posts\scripts\render.py v3/pNN.html --out qa --force --port <yours>`,
jpg + Read. Done = ALL CLEAN without --force AND looks right. Report: file, QA line, one paragraph on the scene.
Don't touch p16 or other posts; don't deliver.
