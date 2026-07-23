# Notes
Node version: v24.13.0
Install frontend dependencies: `npm install`
Install Playwright browser: `npm.cmd run install-browsers`
Install API dependencies: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`
Start API manually: `.\venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000`
Start frontend manually: `npm.cmd run dev`
Run visible automation: `npm.cmd run automate`
Run headless automation: `$env:PLAYWRIGHT_HEADLESS='1'; npm.cmd run automate`
Build email: `npm.cmd run build-email -- --name "Alex" --link "http://localhost:5173" --out out/email.html`
The automation script starts the API/frontend if they are not already running.
Passwords/training codes are never returned by the API or shown in the admin table.
`screenshots/glockapps.png` must come from the external GlockApps dashboard.
