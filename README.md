# Lamar Investment Company Ltd — Website

Django site for Lamar Investment Company Ltd (cleaning services, Kigali),
built per the Swift Results proposal.

## Setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 manage.py migrate
    python3 manage.py createsuperuser   # to manage inquiries via /admin/
    python3 manage.py runserver

Visit http://127.0.0.1:8000/

## Pages

Home, About Us, Our Services, Why Choose Us, Health & Safety, Our Work
(gallery), Contact (contact form saves submissions to the database, visible
at /admin/).

## Partners / companies worked with

The Home page has an "Organizations we've worked with" section. It's driven by
a `Partner` model — add, remove, or reorder partner logos from `/admin/`
without touching any code. Fields: name, logo image, website link (optional),
and a display order. The section is hidden automatically if no partners are
added yet.

## Team photos

The About page has a "The people behind the work" section, driven by a
`TeamMember` model (name, role, photo, order) — same pattern as Partners,
manageable from `/admin/`. It's hidden until at least one team member is
added.

## Seeding the initial team + partners

After `python manage.py migrate`, run:

    python manage.py seed_initial_data

This adds:
- Team: Uwase Jeanine (Operations Manager), Murenzi Charles (Field
  Supervisor), Manzi Jimmy (Cleaning Team Lead) — roles are placeholders,
  edit them from `/admin/` → Team members.
- Partners: RSSB, RBA, NESA — **using plain text-wordmark placeholder logos**
  (not the organizations' official artwork). Replace these from `/admin/` →
  Partners with the real logo files once you have them from each
  organization.
- 3 sample testimonials and 3 sample gallery photos (see below) — also
  placeholders, replace whenever ready.

The command is safe to re-run — it skips anyone already in the database by
name, so it won't create duplicates.

## Email notifications on new inquiries

Every contact-form submission now also sends an email notification (in
addition to saving to the database). By default it just prints the email to
your terminal (`EmailBackend: console`) — zero setup, good for local testing.

To send real emails in production set these environment variables. On
**Railway** (whose cheaper plans block SMTP) use the Resend API:

    RESEND_API_KEY=re_xxxxxxxx
    DEFAULT_FROM_EMAIL=Lamar Investment <info@lamarinvestment.rw>
    LAMAR_NOTIFY_EMAIL=info@lamarinvestment.rw

On a host that allows SMTP you can instead set `EMAIL_BACKEND` to the SMTP
backend plus `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER` and
`EMAIL_HOST_PASSWORD` (see `.env.example`). Notification emails use the
visitor's address as Reply-To. Full setup is in `DEPLOYMENT.md`.

`LAMAR_NOTIFY_EMAIL` is where new-inquiry alerts get sent — set it to
whichever inbox Lamar checks. If sending fails for any reason, the error is
logged but the visitor's inquiry is still saved — a broken email setup will
never block a form submission.

## Our Materials

A new `/materials/` page, matching the pattern of the existing content
models: a `Material` (name, category, optional description, optional
photo, sort order) manageable entirely from `/admin/`. Items are grouped
on the page by category (Equipment & Machines, Cleaning Products &
Chemicals, Consumables & Supplies, Safety & Protective Gear) — a category
with no items simply doesn't appear. Items without a photo show a neutral
placeholder tile instead of a broken image.

It's reachable from the **"Our Work" dropdown** in the navbar (hover or
tap "Our Work" to see both "Our Work" and "Our Materials"), and from the
footer links. It now also comes pre-populated: `python manage.py migrate`
adds the new `Material` table, and `python manage.py seed_initial_data`
(same command used for team/partners/testimonials) adds 15 items across
all four categories — **all 15 now have real product photos** you
provided (see `core/seed_data/materials/`). Safe to re-run; it skips
anything that already exists by name. Replace or add to these from
`/admin/ → Materials` whenever you're ready — send more photos any time
and they can be added the same way, matched to the product they show.

## Navbar

- **"Our Work"** is now a dropdown with two entries: "Our Work" (the
  gallery) and "Our Materials". On desktop it opens on hover; on mobile it
  flattens into an indented sub-list under its own row.
- **Contact Us** is a proper pill-shaped button now (phone icon, shadow,
  lifts slightly on hover) rather than a plain rectangle.
- Between roughly 860–1040px wide, the nav trims itself automatically
  (smaller link text, the "Professional Cleaning Services" tagline
  hides, the phone icon on the Contact button hides) so nothing overflows
  the header before the hamburger menu takes over below 860px.

> **Going live?** See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the Railway deployment steps and pre-launch checklist.

## Brand colours

The whole site (public pages and admin) follows the Lamar brand guide:

| Role | Colour | Where |
| --- | --- | --- |
| Primary blue | `#1C75BC` | buttons, links, icons, CTA banner |
| Blue shades | `#0F4A7A` (deep), `#0A3558` (darker), `#4A93CB` (light) | hero gradients, hovers |
| Blue tints | `#A6C9E4`, `#D1E2F0` | text/accents on dark blue, light button hovers |
| Black & greys | `#111` / `#0F1114`, `#5B6168` | headings, footer, body text |

All of it lives as CSS variables at the top of `core/static/core/css/style.css`
(`--blue`, `--blue-deep`, `--tint`, `--black`, `--ink`, ...) - change a value
there and it updates site-wide. The admin uses `admin-dashboard.css` plus
`admin-theme.css` (loaded via `custom_css` in `JAZZMIN_SETTINGS`). The old
`btn-pill-gold` class is now `btn-pill-light` (white button on blue).

## Nav + hero design (home page)

- **Nav**: links are small uppercase with letter-spacing site-wide. On the
  **home page only**, the header floats transparent over the hero photo with
  the white logo, then turns solid white (dark logo) after you scroll ~40px
  (`core/static/core/js/nav.js`). Inner pages keep the solid white header.
  The home template switches this on with `{% block body_class %}home-page{% endblock %}`.
- **Hero**: full-bleed photo (two real photos that crossfade into each other: `core/static/core/img/hero-1.jpg` and `hero-2.jpg`), a
  frosted-glass card on the left (eyebrow, heading, intro, trust badges), and
  the "See Our Work" / "Explore Our Services" buttons in the bottom-right
  corner. On phones the card goes full width and the buttons stack under it.
- To change the hero photos, just replace `hero-1.jpg` / `hero-2.jpg` (same filenames,
  landscape, ideally 1920px wide or more) - no code changes needed.

## Page hero banners (inner pages)

Every inner page (About, Services, Why Choose Us, Health & Safety,
Gallery, Materials, FAQ, Contact, Privacy) opens with a compact banner:
an eyebrow line, page title, optional one-line subtitle, and a
"Home / Page Name" breadcrumb. **This is colour-only now — no photo** —
a brand-blue gradient with a soft light-blue glow and a masked dot-grid
texture. Each page has its own copy of this markup at the top of its
`{% block content %}` (look for `<section class="page-hero">`), so to
change a title or subtitle just edit the `<h1>` / `<p class="page-hero-lede">`
text directly on that page.

The "Why Choose Us" and "Our Core Values" (About page) cards were also
restyled into hoverable icon cards with a small arrow accent, to match
the same visual language.

## Health & Safety

Redesigned to feel more like a real compliance page: the four badges
(PPE-equipped teams, Site rules followed, etc.) moved out of the content
area into a full-width dark "trust bar" directly under the hero, and the
four-step protocol list is now a 2×2 grid of hoverable icon cards, each
with a large faint watermark number (01–04) in the background — the same
card language used on Services and Why Choose Us.

## Our Services — card grid

Services moved from stacked photo/text rows to a 2-up card grid: each
card has a photo with a floating category badge, a title, a short blurb,
and a check-marked list of what's included. Falls to 1 column on mobile.

The homepage's **"What we take care of"** section used the same old
stacked-row layout with one large, undecorated photo per row — it now
uses the same card grid (photo with floating badge, title, short blurb),
just with a "Learn more" link instead of the full checklist, since it's
a teaser pointing to the Services page rather than the full detail. A
"View All Services" button sits below the grid.

## Footer

The footer has four columns (brand, Links, Working Hours, Get in Touch). The
placeholder newsletter signup bar was removed because it never saved anything.

## Mobile navigation

Fixed: on screens under 860px, the nav now collapses into a hamburger menu
(tap to open a dropdown) instead of disappearing with no way to reach it.

## Chatbot

A simple FAQ chat widget sits in the bottom-left corner of every page
(`core/static/core/js/chatbot.js`). It's rule-based — no API key, no external
service, no ongoing cost. It matches visitor questions against a small set of
FAQs (services, coverage area, quotes, supplies, health & safety, booking,
contact) by keyword, with quick-reply buttons for the most common ones. To
add or edit a question, edit the `faqs` array at the top of that file — each
entry has `keywords`, `question`, and `answer`.

## Spam protection

The contact form has a honeypot field (`website`) that's invisible to real
visitors (hidden off-screen via CSS, not `display:none`, so bots that only
skip obviously-hidden fields still get caught). If it comes back filled in,
the submission is silently discarded — the visitor still sees the normal
"thanks" message, so bots don't learn they were blocked, but nothing is
saved or emailed. No configuration needed.

## WhatsApp button

A green WhatsApp button appears on the **Contact page only** (not site-wide —
the chat bot stays site-wide, bottom-left). It opens a chat pre-filled with a
quote request message, using **+250 724 685 138**.

## Testimonials

The Home page has a "What clients say" section, driven by a `Testimonial`
model (client name, detail like company/neighbourhood, an **optional photo**,
quote, 1–5 star rating, order) — manageable from `/admin/`. The photo can be
a picture of the client or their company logo; if left blank, the
testimonial just shows without one. Currently seeded with 3 sample
testimonials (Jean Paul K., Aline Uwase, Diane M.) — **these are placeholder
quotes, written to show the layout working. Replace them with real client
feedback from `/admin/` whenever you have some.**

## Adding images/logos in the admin

Partners, Team members, Testimonials, and Work photos all have an image
upload field, and the admin list view for each now shows a small thumbnail
preview so it's easy to see at a glance what's already uploaded:

- **Partners** → Logo (required)
- **Team members** → Photo (required)
- **Testimonials** → Photo (optional — client photo or company logo)
- **Work photos** → Image (required)

To add one: go to `/admin/`, pick the relevant section under "Core", click
"Add", fill in the fields, and choose an image file. Save, and it appears on
the live site immediately.

## Our Work gallery

A page (`/gallery/`, linked in the nav) for real job photos, driven by a
`WorkPhoto` model. Each photo has a category (Before / After / General
work). Give a "before" and "after" photo the same `pair_key` (e.g.
`office-oct-2026`) in the admin and they'll display side-by-side
automatically; anything without a matching pair shows as a single photo.

Currently seeded with 3 cleaning-service stock photos (office cleaning, a
cleaning team, and residential vacuuming) — these are **stock photography,
not actual photos of Lamar's own jobs**. They're a reasonable placeholder
since they're genuinely photos of cleaning work rather than text graphics,
but swap them for real job photos from `/admin/` as soon as you have them —
worth doing sooner rather than later, since a client who reverse-image-
searches a stock photo and finds it's generic could raise an eyebrow.

## Social links

Footer icons link to the official accounts:
- Instagram: `instagram.com/lamarinv`
- Facebook: `facebook.com/profile.php?id=61594232766192`
- X: `x.com/lamarinves`

## Production settings

`DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` are now environment-variable
driven — safe defaults for local dev (just run `manage.py runserver`, no
setup needed), real values expected in production. See `.env.example` for
the full list. The important ones:

    DJANGO_SECRET_KEY=<generate a real one>
    DJANGO_DEBUG=False
    DJANGO_ALLOWED_HOSTS=lamarinvestment.rw,www.lamarinvestment.rw

Generate a real secret key with:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

When `DJANGO_DEBUG=False`, a set of production security settings turn on
automatically (secure cookies, HSTS, clickjacking protection, HTTPS
redirect). These assume the site is served over HTTPS, which any real host
(Render, Railway, a VPS with Let's Encrypt, etc.) should provide.

Also run `python manage.py collectstatic` once before deploying — it
gathers all static files (CSS/JS/images) into `staticfiles/` for your web
server to serve directly. Needed in production; not needed for
`runserver` locally.

## Privacy Policy page

A `/privacy/` page is linked from the footer (not the main nav, to keep
that uncluttered). Covers what the contact form collects, how it's used,
and how someone can ask to have their data corrected or removed — written
for the fact that this site only collects contact-form details, nothing
more. Update the wording in `core/templates/core/privacy.html` if that
changes.

## Favicon

Generated from the top "LC" mark of the logo (cropped, not the full
wordmark, since a favicon needs to read at a tiny size). Files are in
`core/static/core/img/`: `favicon.ico`, `favicon.png`, and
`apple-touch-icon.png`. Regenerate from a cleaner source logo file later if
you want a sharper result — the current one is cropped from the same JPEG
used elsewhere on the site.

## Google Maps embed

The Contact page now embeds a Google Map pinned to **CPR-Unity House, KK21,
Niboye, Kicukiro, Kigali, Rwanda** (the address is also updated in the
footer and the Contact page's location text). This uses Google's free
no-API-key embed — no billing setup or API key needed. If you want a more
precise pin (this one geocodes the address text, which is usually accurate
but not pixel-exact), let me know and I can switch it to exact coordinates.

## Service images

Each service category on the Services page (and its preview on the Home
page) now has a photo:

- **Commercial** → office interior
- **Residential** → modern apartment building
- **Institutional** → large office tower
- **Specialized** → two event-venue photos side by side (fits "post-event
  cleaning" well)

**Note on Institutional**: none of the supplied images actually show a
school or clinic (what the copy describes) — the office tower is used as
the closest available stand-in for "large facility." If you get an actual
school/clinic photo later, swap it in at
`core/static/core/img/services/institutional-classroom.jpg` (the Institutional card now cycles `institutional-classroom`, `-factory` and `-cleaning`) (same filename, so no
template changes needed).

These are plain static files, not admin-editable — to change one, replace
the file at `core/static/core/img/services/<name>.jpg` with a new image
using the same filename, or edit the `<img src>` paths in
`core/templates/core/services.html` and `home.html` to point elsewhere.

## Social sharing (Open Graph / Twitter cards)

When someone shares a link to the site on WhatsApp, Facebook, or X, it now
shows a proper preview: title, description, and a branded image
(`core/static/core/img/og-image.jpg`, auto-generated from the logo — swap it
for a nicer designed version whenever you want). Per-page titles/descriptions
can be customized by overriding the `og_title` / `og_description` blocks in
any template, though every page currently just uses the site-wide default.

## Custom 404 page

A branded "Page not found" page (`core/templates/404.html`) now shows for
broken links instead of Django's default error page. **Only visible when
`DJANGO_DEBUG=False`** — with debug mode on (the local default), Django
shows its own detailed debug page instead, which is expected and correct
for local development.

## robots.txt and sitemap.xml

Both are now served automatically at `/robots.txt` and `/sitemap.xml` —
nothing to configure. This helps search engines actually find and index the
site. The sitemap lists all 8 public pages; if you add a new page later,
add it to the `urls` list in the `sitemap_xml` view in `core/views.py`.

## Business hours

Shown in the footer (every page) and on the Contact page: **open daily,
7:00 AM – 7:00 PM**. To change it, it's plain text in both
`core/templates/core/base.html` and `core/templates/core/contact.html` —
no model behind it, just search for "7:00 AM" in each file.

## Analytics (Google Analytics / GA4)

Off by default — no tracking script loads until you set a real Measurement
ID. To turn it on:

1. Go to [analytics.google.com](https://analytics.google.com), create a
   property for the site (or use an existing one), and find your
   **Measurement ID** under Admin → Data Streams → your web stream. It
   looks like `G-XXXXXXXXXX`.
2. Set the environment variable:

       GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

3. Restart the server. The tracking snippet now loads on every page.

The Privacy Policy page already mentions that analytics may be used, so
nothing else needs updating when you turn this on.

## FAQ page

A crawlable `/faq/` page (linked from the footer's Explore list) covering
the same ground as the chatbot — services, coverage area, pricing,
supplies, safety, booking, hours, and contact details. Unlike the chatbot
(which only responds to a visitor's click), this is plain page content
Google can actually index, which helps people find the site via search.
Edit the Q&A pairs directly in `core/templates/core/faq.html`.

## Admin dashboard theme

The `/admin/` backend now uses [django-jazzmin](https://django-jazzmin.readthedocs.io/)
for a proper dashboard look instead of Django's plain default admin:
branded login page and sidebar (Lamar logo, green theme), a left-hand
navigation menu with icons per section (Inquiries, Team members, Partners,
Testimonials, Work photos), a top search bar, and a "View Site" shortcut.
Model order in the sidebar is set so Inquiries — the thing you'll check
most — is first.

New dependency: `django-jazzmin` (already in `requirements.txt`, installs
with the rest via `pip install -r requirements.txt`). All the settings for
colors/icons/branding live in `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS` in
`lamar_project/settings.py` if you ever want to adjust them — e.g. change
`"theme"` for a different overall look, or edit the `"icons"` dict to swap
any model's icon (uses [Font Awesome](https://fontawesome.com/icons) class
names).

### Dashboard stats overview

The admin homepage now opens with 6 live stat cards, styled to match the
public site's brand (same fonts/colors, not generic Bootstrap blue):
**New inquiries** (unhandled — highlighted in gold since it's the one to
watch), Total inquiries, Team members, Partners, Testimonials, and Gallery
photos. Each card is clickable and jumps straight to that list in the
admin. New inquiries updates automatically as they come in — no manual
refresh logic needed, it's just a live database count on each page load.

How it's built, if you ever want to add another stat card: `core/admin.py`
wraps the built-in admin homepage view to compute the counts and inject
them into the template context (`lamar_stats`); the actual cards are
rendered in `templates/admin/index.html` (a project-level override — this
directory takes priority over Jazzmin's own version of that page, set via
`TEMPLATES` → `DIRS` in `settings.py`); the styling lives in
`core/static/core/css/admin-dashboard.css`.

## CSV export for inquiries

In `/admin/` → Inquiries, select one or more rows, choose "Export selected
inquiries as CSV" from the action dropdown, and click Go. Downloads a CSV
with all the inquiry details — handy for opening in Excel or sharing with
someone who doesn't have admin access.

## Before launch — please check

- ~~Name discrepancy~~ **Resolved**: an earlier logo file read "LAMAL", but a
  corrected logo (confirming "LAMAR Investment Company Ltd") has since been
  provided; that has now been replaced by the final chosen logo (see "Logo"
  below).
- ~~Placeholder email/phone~~ **Resolved**: using the real email
  (info@lamarinvestment.rw) and phone (+250 799 529 500)
  sitewide, including WhatsApp.
- Set the production environment variables above before deploying (`.env.example`
  has the full list).
- Domain, hosting, and SEO setup from the proposal are deployment-stage
  tasks — happy to help wire those up once you've picked a host.
- **Our Materials starts with 15 items, all with real product photos**
  you provided (seeded via `seed_initial_data`, see above). Swap any of
  them out, add more, or edit the descriptions from `/admin/` whenever
  you like.

## Responsive design (phones, tablets, desktops)

Tested with a headless browser at 280, 320, 360, 390, 412, 600, 768, 820, 1024,
1280 and 1920px wide, plus landscape phones, on every page — no horizontal
scrolling anywhere. The responsive rules live in the last sections of
`core/static/core/css/style.css` ("Responsive hardening").

- **Phones (up to 860px)**: hamburger menu (closes on link tap, outside tap or
  Escape; scrolls if the screen is short), 44px+ tap targets, 16px form fields
  so iOS doesn't zoom on focus, safe-area padding for notched phones.
- **Tablets**: touch iPads/tablets get tap-to-open dropdowns ("About Us",
  "Our Work" > Our Materials) — first tap opens, second tap follows the link.
- **Very small screens (360px and under)**: tighter header, single-column grids.
- **Chat + WhatsApp buttons**: smaller on phones, kept clear of the home
  indicator, and hidden while the mobile menu is open.
- Also fixed: the chatbot still showed placeholder contact details; it now
  uses the real email and phone.

## Logo

The site uses the final chosen logo (blue "L" mark + LAMAR / INVESTMENT COMPANY),
from `Lamar_Chosen_Logo.pdf`. Files in `core/static/core/img/`:

- `logo.png` - horizontal version, header (transparent background)
- `logo-light.png` - all-white version of the same, footer (dark green background)
- `logo-stacked.png` - stacked version, admin login page
- `favicon.ico`, `favicon.png`, `apple-touch-icon.png` - the "L" mark only
- `og-image.jpg` - 1200x630 social-sharing preview (WhatsApp / Facebook / X)

The header no longer repeats the company name as text, since the logo already
contains it. The logo is blue while the rest of the site is forest green and
gold; if Lamar wants the site to match the logo, the colours are the CSS
variables at the top of `core/static/core/css/style.css` (`--forest`, `--gold`, ...).
#   l a m a r  
 