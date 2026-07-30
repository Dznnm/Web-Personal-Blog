# Vale's Blog

#### Project URL: <(https://roadmap.sh/projects/personal-blog)>

## Description

Vale's Blog is a simple personal blogging platform built with Flask. It lets a single admin user write, edit, and delete articles through a password-protected dashboard, while anyone visiting the site can read published articles without needing an account.

The project was built as a way to apply backend fundamentals learned so far — routing, Jinja templating, sessions, authentication, and password hashing — in a small but complete full-stack application, rather than jumping straight into a database-backed project. Article data is currently stored in a local `articles.json` file, which keeps the project easy to read and reason about while the focus stays on backend logic and the request/response cycle. A move to SQLite/PostgreSQL is planned as the next phase of development.

## Features

- **Public blog view** — anyone can browse the home page and read individual articles without logging in.
- **Admin login** — a single admin account, defined via environment variables, protects all write operations.
- **Session-based authentication** — Flask's `session` object tracks whether an admin is logged in; protected routes redirect to `/login` if not.
- **Password hashing** — the admin password is never stored or compared in plain text; `bcrypt` is used to hash and verify it.
- **Full CRUD for articles** — the admin can create, read, update, and delete articles from the dashboard.
- **Separate guest/admin views** — logged-out visitors see a read-only article page (`article_guest.html`), while the admin sees an editable version with Edit/Delete controls (`article.html`).
- **Confirmation on delete** — the dashboard asks for confirmation (via a JavaScript `confirm()` prompt) before deleting an article, to help prevent accidental data loss.

## File Structure

| File | Description |
|---|---|
| `app.py` | Main Flask application: routes, session handling, article CRUD logic, and password hashing helpers. |
| `articles.json` | Local JSON "database" storing all articles as a list of objects (`id`, `title`, `content`, `date`). Created automatically on first save if it doesn't exist. |
| `templates/home.html` | Public homepage listing all articles, linking to the guest article view. |
| `templates/article_guest.html` | Read-only article view shown to visitors who are not logged in. |
| `templates/dashboard.html` | Admin-only page listing all articles with Edit/Delete controls and a link to add a new article. |
| `templates/article.html` | Admin-facing article view with Edit and Delete actions. |
| `templates/add_article.html` | Form for creating a new article. |
| `templates/edit_article.html` | Form for editing an existing article's title and content, pre-filled with current values. |
| `templates/login.html` | Admin login form; displays an error message on invalid credentials. |
| `static/css/style.css` | Stylesheet shared across all pages — handles layout, typography, forms, and buttons. |
| `.env` | Local environment file (not committed) storing `ADMIN_USERNAME`, `ADMIN_PASSWORD` (hashed), and `SECRET_KEY`. |

## How It Works

**Guest routes**
- `/` — home page, lists all articles.
- `/article/<article_id>` — read-only view of a single article.

**Login routes**
- `/login` — GET shows the login form; POST checks the submitted username/password against the admin credentials (using `bcrypt.checkpw`) and starts a session on success.
- `/logout` — clears the session and logs the admin out.

**Admin routes** (all require an active session; otherwise redirect to `/login`)
- `/dashboard` — lists all articles with Edit/Delete options and a link to add a new one.
- `/articled/<article_id>` — admin view of a single article with Edit/Delete actions.
- `/add_article` — GET shows the "New Article" form; POST creates a new article with an auto-incremented `id` and today's date, then saves it to `articles.json`.
- `/edit_article/<article_id>` — GET shows the edit form pre-filled with the article's current data; POST either updates the article's title/content or deletes the article, depending on which button was submitted.

## Design Choices

- **JSON over a database, for now.** Since the current learning focus is backend fundamentals (routing, sessions, auth) rather than data modeling, using a JSON file keeps the storage layer simple and transparent while those concepts are being built up. SQL is the next planned phase.
- **Single hardcoded admin instead of a user table.** The blog is meant for one author, so a full user-registration system would have added complexity without adding value at this stage. Credentials live in environment variables, and the password is hashed rather than stored in plain text.
- **Separate templates for guest vs. admin article views.** Rather than using conditional logic inside a single template to show or hide Edit/Delete controls, the project uses two templates (`article.html` and `article_guest.html`) to keep each template focused and easy to read.

## Setup

1. Clone the repository and install dependencies:
   ```
   pip install flask bcrypt python-dotenv
   ```
2. Create a `.env` file in the project root with:
   ```
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_bcrypt_hashed_password
   SECRET_KEY=your_secret_key
   ```
3. Run the app:
   ```
   flask run
   ```
   or
   ```
   python app.py
   ```
4. Visit `http://127.0.0.1:5000` to view the blog, or `/login` to sign in as admin.

## Known Limitations / Future Improvements

- Article storage will be migrated from `articles.json` to SQLite/PostgreSQL.
- The app is not yet deployed; deployment (Gunicorn + a hosting service) is planned as a later phase.
- Only a single admin account is supported; there is no multi-user or role system.
- No automated tests yet — all routes have been tested manually.

## Author

Dzannun