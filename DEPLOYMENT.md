# Deploying the Lamar website on Railway

Contact email used everywhere: **info@lamarinvestment.rw**

> I could not run Django where these files were prepared (no internet, Django not
> installed), so the production settings, `start.sh` and the email backend are
> **untested**. Step A1 below is the first real test - do it before anything else.

---

## A. Do these BEFORE deploying

1. **Test on your computer.**
   ```
   pip install -r requirements.txt
   python manage.py test            # 13 checks: every page loads + email backend
   python manage.py collectstatic --noinput
   ```
   If anything fails, send me the error before going further.
2. **Put the code on GitHub** (Railway deploys from there). `.gitignore` already keeps
   `db.sqlite3`, `media/` and `.env` out - good, they must not be uploaded.
3. **Create the accounts:** Railway (paid plan needed for a permanent Volume - check
   current plans), and a free-to-start **Resend** account for sending email (see D).
4. **Domain access:** you need to edit DNS records for `lamarinvestment.rw`
   (at your registrar / wherever the domain's DNS is managed).
5. **The mailbox must exist.** Inquiries are emailed *to* info@lamarinvestment.rw, so that
   address needs a real inbox (Google Workspace, Zoho Mail, your registrar's mailbox, or a
   forward to a Gmail you read). Creating the address in Resend does NOT create an inbox.
6. **Decide about the placeholder testimonials.** On the first start the site loads its starting
   content, including the 3 sample testimonials (Jean Paul K., Aline Uwase, Diane M.). They are
   invented. To keep them off the live site, delete the `TESTIMONIALS = [...]` entries in
   `core/management/commands/seed_initial_data.py` (leave `TESTIMONIALS = []`) *before* the first
   deploy - or delete them in `/admin/` afterwards.
7. Generate a secret key and keep it safe:
   `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

What the first start loads automatically: your real **team (4)**, **partners (5)**, the
**materials**, and the **Our Work** photos - the same as on your computer. Your local
database is NOT uploaded (it contains a test inquiry and your local admin).

---

## B. Set up Railway

1. **New Project -> Deploy from GitHub repo** -> pick the repository.
2. **Attach a Volume** to the service, mount path `/data`. This is where the database and
   uploaded photos live. *Without a volume everything is wiped on every deploy.*
3. **Variables tab** - add (see `.env.example` for the full list):
   | Variable | Value |
   | --- | --- |
   | `DJANGO_SECRET_KEY` | the key from A7 |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | `lamarinvestment.rw,www.lamarinvestment.rw` |
   | `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD` / `DJANGO_SUPERUSER_EMAIL` | your first admin login (use a long password; email `info@lamarinvestment.rw`) |
   | `RESEND_API_KEY` | from step D |
   | `DEFAULT_FROM_EMAIL` | `Lamar Investment <info@lamarinvestment.rw>` |
   | `LAMAR_NOTIFY_EMAIL` | `info@lamarinvestment.rw` |
4. **Deploy.** `start.sh` runs the database setup, collects the static files, loads the starting
   content (once), creates your admin, then starts the site. Watch the deploy logs.
5. **Settings -> Networking -> Generate Domain** to get a `*.up.railway.app` address. Open it and
   check the site works (that address is allowed automatically).
6. **Custom domain:** in the same Networking section add `lamarinvestment.rw` and
   `www.lamarinvestment.rw`. Railway shows the exact DNS records to create; add them at your DNS
   provider. HTTPS is issued automatically once DNS points correctly. (Apex/root domains need a
   registrar that supports CNAME flattening/ALIAS; if yours doesn't, use `www` as the main
   address and redirect the bare domain to it.)
7. **After the first successful start, delete `DJANGO_SUPERUSER_PASSWORD`** from the variables
   (it is only used once), then log in at `/admin/`.

## C. Why email goes through Resend, not Gmail/SMTP
Railway's Free, Trial and Hobby plans **block SMTP** (ports 25/465/587), so a normal mail server
login would silently fail there. Railway recommends an email service with an HTTPS API
(Resend, SendGrid, Mailgun, Postmark). The site includes a small Resend backend
(`core/email_backends.py`); setting `RESEND_API_KEY` switches it on. (On the Pro plan SMTP also works.)

## D. Resend setup
1. Create a Resend account -> **Domains -> Add Domain** -> `lamarinvestment.rw`.
2. Add the DNS records Resend shows (at your DNS provider) and click **Verify**.
3. **API Keys -> Create** (sending access) -> paste it into `RESEND_API_KEY` in Railway.
4. Test: submit the Contact form on the live site. The message should appear in `/admin/` *and*
   arrive at info@lamarinvestment.rw (hit Reply - it goes straight to the visitor).
If the email doesn't arrive, the inquiry is still saved in `/admin/`; check Railway's logs.

---

## E. Launch checklist
- Click through every page on the live domain (logo, photos, footer, WhatsApp button, map).
- Contact form test (D4). Log in to `/admin/`, upload a test photo to Our Work, confirm it shows, delete it.
- `/robots.txt` and `/sitemap.xml` show your real domain.
- Submit the sitemap in Google Search Console; create a Google Business Profile.
- Share the link on WhatsApp/Facebook to check the preview image.
- Still placeholders to fix in `/admin/`: team roles (confirm), partner logos (only show organisations that
  agreed), Privacy page wording, stock/AI photos on service cards.

## F. Running it day to day
- **Update the site:** push to GitHub; Railway redeploys. Redeploying a service with a volume may
  cause a short interruption - normal.
- **Content changes** (team, partners, photos, testimonials) are done in `/admin/` and are stored on the volume.
- **Backups:** your data is one SQLite file + photos on the volume. Turn on Railway's volume backups
  if your plan offers them, and now and then download the `db.sqlite3`/`media` contents.
- Keep the service at **1 replica** (SQLite allows a single writer).
- If the site ever grows, the next step is Railway's PostgreSQL + a storage bucket for photos.

## G. Other hosts
`deploy/` contains Nginx/systemd/backup files for a plain Ubuntu VPS if you ever leave Railway.
