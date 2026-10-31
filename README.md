# Anonymous Message Site

A simple Flask app that lets people send anonymous messages and lets you view/delete them from an admin page.

## Run locally

```bash
git clone https://github.com/Jacobtuss2/anonymous-message-site.git
cd anonymous-message-site
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open:
- http://localhost:5000
- http://localhost:5000/admin

## Notes

- Messages are stored in a local SQLite database called `messages.db`
- This is a beginner-friendly local project
- It is not protected for public internet use yet
