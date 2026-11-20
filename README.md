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

- **Diaesityksen kuvat**: add up to four photos, assign each a unique slot
  (`01`–`04`), and publish them to show them in the homepage hero. Slideshow
  photos are managed separately from portfolio photos.
- **Portfolio-luvut**: create, delete, and order the chapters shown on the
  Portfolio page, such as Hääkuvat, Perhekuvat, or Parikuvat. Change a
  chapter's **Display order** in the list to move it. Publish a chapter to show
  it. Open a chapter to add, edit, publish, reorder, or delete its photos
  directly in the chapter editor.
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
- **Contact links**: add or edit links such as Instagram under
  **Yhteystietolinkit**. Use “Is published” and “Display order” to control
  which links appear and their order.

The frontend must also be running (`npm run dev`) to preview these changes.
Install backend dependencies from the `backend` folder with
`pip install -r requirements.txt`. Set `DJANGO_SECRET_KEY` in the environment
for any hosted environment; the development fallback in settings is not for
production.

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
