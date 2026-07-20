# Fullstack Developer Assessment — Candidate Brief

Welcome. This is a **5-day, beginner-level coding assessment** for a **fullstack developer** role. You will build a small end-to-end product slice: a pixel-faithful login UI, a form-submission API, an admin panel, a phishing-style HTML email, and a browser automation script.

We care about **working fullstack code** and **attention to visual detail**. We are not grading design originality — we are grading how well you recreate a real UI, wire it to a backend, and ship something that runs.

---

## What you receive

You will receive **one website URL**. That live page is your only design reference.

- No Figma file
- No asset pack
- No copy sheet

Open the site, inspect it, and build what you see.

---

## What you will build

Across three phases you will deliver:

1. **Frontend** — Vue 3 clone of the given site's login page
2. **Backend** — API to accept submissions, list them, and toggle the form live or stopped
3. **Admin UI** — simple admin view that looks like it belongs to the same product
4. **Email** — HTML phishing email that looks like it came from the same product, tested for deliverability
5. **Automation** — browser automation script that runs the full user journey without manual input

---

## Rules (all phases)

1. **Frontend stack:** Vue 3 + Vite. Use the Composition API — the `<script setup>` style is preferred.
2. **No React** (or Preact, Next, etc.). This is intentional — many candidates know React, and we want to see you adapt.
3. **No UI component libraries** like Vuetify, Quasar, or Element Plus. Write your own HTML and CSS.
4. **No iframes** of the original site. Rebuild the UI yourself.
5. **Do not copy their CSS or JS files** into your project. Write your own styles locally.
6. **Do not call their real login API.** Your backend runs locally only.
7. Stay on the given site's visual style. Do not invent a different brand look.
8. Never print passwords in logs or show them in the admin panel.

Backend language is your choice — Node/Express or Python/FastAPI both work fine.

---

## Schedule

| Day | Phase | Focus |
|-----|-------|--------|
| 1 | [Phase 1](./PHASE-1.md) | Desktop Vue clone of the given site |
| 2 | [Phase 1](./PHASE-1.md) | Interaction states, narrow viewport, wire form to API |
| 3 | [Phase 2](./PHASE-2.md) | Submission API, admin panel, Live/Stopped |
| 4 | [Phase 2](./PHASE-2.md) | HTML phishing email + GlockApps deliverability test |
| 5 | [Phase 3](./PHASE-3.md) | Browser automation script + final consistency pass |

Expect around **4 to 6 hours per day**. Finish the core path cleanly. Polish if you have time.

---

## How we evaluate

| Area | What good looks like |
|------|----------------------|
| UI fidelity | Side-by-side with the live site, hard to tell apart |
| Fullstack wiring | Form submits, saves, and shows in admin |
| Adaptability | Real Vue — not a React app in disguise |
| Product sense | Live/Stopped works, empty states handled, consistent branding |
| Automation | Script runs the full journey start to finish without manual input |

---

## How phase reviews work

This assessment runs as a **gate process**. You submit at the end of each phase, and we review before you are allowed to continue.

- **End of Day 2 (Phase 1):** Submit your work. We will review your Vue clone and backend stub. If it meets the bar, we send you Phase 2 and you continue to Day 3. If it does not, the assessment ends here.
- **End of Day 4 (Phase 2):** Submit again. We review your admin panel and email. If it meets the bar, we send you Phase 3 and you continue to Day 5. If it does not, the assessment ends here.
- **End of Day 5 (Phase 3):** Submit your final work. This is the last review.

You will hear back from us **within 24 hours** of each submission.

Do not rush ahead. A Phase 1 that barely works will not unlock Phase 2. Solid work at each step is more important than racing to the finish.

---

## How to submit at the end of each phase

Push your work to a private git repository and share access with us, or send a git bundle. Tag your commit before you send:

- End of Phase 1: `git tag phase-1-submit`
- End of Phase 2: `git tag phase-2-submit`
- End of Phase 3: `git tag assessment-final`

In your message include:

- Which phase you are submitting
- The exact commands to install and run what you built
- Your day notes file (`DAY2.md` for Phase 1, `DAY4.md` for Phase 2, `NOTES.md` for Phase 3)

---

Read the phase file before you start each phase. When you are ready, begin with [Phase 1](./PHASE-1.md).
