# Anonymous Message Site

A simple Flask app that lets people send anonymous messages and lets you view/delete them from an admin page.

## Run locally

```bash
git clone https://github.com/Jacobtuss2/anonymous-message-site.git
cd anonymous-message-site
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:
- http://localhost:5000
- http://localhost:5000/login

## Admin password

You can set a strong password before starting the app with:

```bash
export ADMIN_PASSWORD='Y0ur_Str0ng_P@ssw0rd!2026'
python app.py
```

If `ADMIN_PASSWORD` is not set, the app uses a development default, but you should replace it in production.

## Notes

- Messages are stored in a local SQLite database called `messages.db`
- Passwords are checked using Werkzeug's hashed password support (`scrypt`), not plain text
- This is a beginner-friendly local project
- It is not yet public on the internet without deployment hosting
