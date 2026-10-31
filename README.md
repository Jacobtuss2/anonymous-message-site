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
- http://localhost:5000/admin

## Admin password

The default admin password is:

```bash
admin123
```

You can change it before starting the app with:

```bash
export ADMIN_PASSWORD=mysecretpassword
python app.py
```

## Notes

- Messages are stored in a local SQLite database called `messages.db`
- This is a beginner-friendly local project
- It is not yet public on the internet without deployment hosting
