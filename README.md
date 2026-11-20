# Hiltunen Photography

A React and Vite portfolio site for Hiltunen Photography.

## Start the project

Open a terminal in this folder and run:

```sh
npm install
npm run dev
```

Open the local address Vite prints in the terminal. The browser refreshes when
you save a change.

## Edit site content

Slideshow photos, portfolio chapters and photos, About content, service prices,
and non-homepage text are managed in Django Admin. Page layouts remain fixed in
the frontend.
Start the Django backend from the `backend` folder with:

```sh
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` and sign in with a Django staff account.
An administrator can create one with `python manage.py createsuperuser`.
You can also open **Ylläpito** from the website's menu.
The Admin home groups common tasks into simple cards; expand **Kaikki
hallintanäkymät** to see the full list of editable content types.

- **Diaesityksen kuvat**: add up to four photos, assign each a unique slot
  (`01`–`04`), and publish them to show them in the homepage hero. Slideshow
  photos are managed separately from portfolio photos.
- **Portfolio-luvut**: create, delete, and order the chapters shown on the
  Portfolio page, such as Hääkuvat, Perhekuvat, or Parikuvat. Upload an
  optional **Kansikuva** for each chapter; until one is added, its first
  published photo is used as the cover. Visitors can open a chapter card to
  view and scroll through its photos. Change a chapter's **Display order** in
  the list to move it. Open a chapter in Admin to add, edit, publish, reorder,
  or delete its photos.
- **Portfolio-kuvat**: photos can also be managed from this separate list.
  Only published photos in published chapters appear on the Portfolio page;
  these photos do not appear on the homepage.
- **About content**: edit the homepage introduction and About page text and
  upload its main image. Manage the additional About page images under
  **Minusta-sivun kuvat** by adding their public image URLs, alt text, and
  display order.
- **Services**: edit service names, descriptions, and displayed prices. Use
  “Is published” and “Display order” to control what appears and in what order.
- **Other page text**: edit the headings, labels, and empty-state messages for
  Portfolio, Services, About, and Contact under **Muiden sivujen tekstisisältö**.
- **Contact links**: fill in the prepared Website, Facebook, TikTok, WhatsApp,
  and Pinterest entries under **Yhteystietolinkit**, or add another link.
  Add a full URL for websites and social accounts. For WhatsApp, choose
  “WhatsApp-puhelinnumero” and enter the number with its country code; the site
  creates the WhatsApp link automatically. Use “Is published” and “Display
  order” to control which links appear and their order. Empty links stay hidden.

The frontend must also be running (`npm run dev`) to preview these changes.
Install backend dependencies from the `backend` folder with
`pip install -r requirements.txt`. Set `DJANGO_SECRET_KEY` in the environment
for any hosted environment; the development fallback in settings is not for
production.

## Temporary client demo

Start Django locally on `127.0.0.1:8000`, then run these commands from the
project root:

```sh
npm run build:demo
npm run preview:demo
```

In another terminal, create a temporary public link:

```sh
cloudflared tunnel --url http://127.0.0.1:4173
```

Share the `trycloudflare.com` URL printed by Cloudflare. The demo build hides
the Admin link, and its preview server proxies only the public API and media.
Keep Django, Vite Preview, and Cloudflare Tunnel running while the client views
the demo; the public link expires when the tunnel stops.

## Learn the files

- `src/main.jsx` starts React and displays the `App` component.
- `src/App.jsx` is the top-level component. It currently displays the homepage.
- `src/sivut/Etusivu.jsx` contains the homepage content.
- `src/App.css` contains styles for the page sections.
- `src/index.css` contains global styles such as fonts and page defaults.

### Change text

Open `src/sivut/Etusivu.jsx` and edit the text between JSX tags. For example:

```jsx
<h1>
  Valokuvia,
  <br />
  jotka <em>tuntuvat.</em>
</h1>
```

`h1` is a large heading, `br` starts a new line, and `em` emphasizes text.

### Change appearance

Each HTML element can have a `className`, such as `className="hero"`. Find the
matching `.hero` rule in `src/App.css` to change how it looks. In CSS, a dot
before a name selects a class.

## Build the site

Run `npm run build` to create the production version in the `dist` folder.

## Prepare the production launch

The root `render.yaml` and `Dockerfile` define one Render web service in
Frankfurt, a managed PostgreSQL database, and a persistent disk for uploaded
media. These are paid resources; review Render's current pricing before
applying the Blueprint.

1. Push the deployment files to the GitHub `main` branch.
2. In Render, create a new Blueprint from this repository and apply
   `render.yaml`. The build creates the React assets, collects Django static
   files, and runs migrations before startup.
3. Buy the `.fi` domain from a domain registrar and add it to the Render web
   service's **Custom Domains**. Set `DJANGO_ALLOWED_HOSTS` to the exact
   hostname(s), for example `example.fi,www.example.fi`; the matching HTTPS
   origins are added to Django's CSRF settings automatically.
4. Create the production administrator from the Render Shell:

   ```sh
   cd backend && python manage.py createsuperuser
   ```

The Render database starts empty apart from migrations. Existing content in
the local SQLite database and uploaded files under `backend/portfolio/` are
not included in Git, so they must be migrated to production before the site
goes live. The `DJANGO_SECRET_KEY` is generated by Render and should never be
committed.

Uploaded images are stored on Render's persistent disk. Configure SMTP
variables (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD`, and `EMAIL_USE_TLS`) in Render if Django admin password
reset emails are needed; the site does not send reservation emails.
