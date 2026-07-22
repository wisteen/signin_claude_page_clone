Build the sample email:
`npm run build-email -- --name "Alex" --link "http://localhost:5173" --out out/email.html`

Allowed link hosts: `localhost`, `127.0.0.1`, `::1`, and `lab.local`.
The script rejects non-local or non-lab hosts.

Open `out/email.html` in a browser to review the rendered email.
This is a local training email and should not be sent to real users.

GlockApps: not run from this workspace because it requires signing in and sending from an email account.
If required by the instructor, send only to GlockApps test addresses and save the result screenshot as `screenshots/glockapps.png`.
