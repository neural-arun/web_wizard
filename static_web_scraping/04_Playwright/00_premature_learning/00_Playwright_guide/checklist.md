
# ✅ PLAYWRIGHT — DAILY EXECUTION CHECKLIST

---

## 🧠 Day 0 — Dynamic X-Ray (NO CODE DAY)

**Goal:** Decide *how* the site gives data.

**Checklist**

* [ ] Open DevTools → Network → XHR/Fetch
* [ ] Trigger the action (scroll / search / click)
* [ ] Identify **actual data source**:

  * [ ] HTML
  * [ ] XHR JSON API
  * [ ] GraphQL
  * [ ] Cursor / pagination
  * [ ] Token / cookie based
* [ ] Write 4 lines in notes:

  ```
  Site:
  Data Source:
  Auth Type:
  Best Tool:
  ```
* [ ] Decision made in **≤ 10 min**

**Done when:**
You can explain the data flow in one sentence.

---

## 🖱️ Day 1 — Drive the Browser

**Goal:** Automate a real flow without hacks.

**Checklist**

* [ ] `playwright install` works
* [ ] Run `playwright codegen <site>`
* [ ] Record: open → action → data visible
* [ ] Replace fragile selectors:

  * [ ] ❌ XPath
  * [ ] ✅ role / text / data-attr
* [ ] Script runs **twice** without change
* [ ] ❌ No `time.sleep`

**Done when:**
Script survives refresh + rerun.

---

## ⏳ Day 2 — Stability (Scrolls & Waits)

**Goal:** Never hang or loop forever.

**Checklist**

* [ ] Replace sleeps with:

  * [ ] `wait_for_selector`
  * [ ] `networkidle` (only if valid)
* [ ] Infinite scroll loop:

  * [ ] Detect **new items**
  * [ ] Stop when no new IDs appear
* [ ] Add:

  * [ ] Screenshot on crash
  * [ ] Save HTML on crash

**Done when:**
Script stops by itself and leaves evidence if it fails.

---

## 🔐 Day 3 — Login Once, Reuse Safely

**Goal:** Avoid logging in every run.

**Checklist**

* [ ] Headed login works
* [ ] `auth.json` saved
* [ ] Reuse `storage_state`
* [ ] Detect expiry:

  * [ ] Redirect to `/login` OR
  * [ ] Login selector appears
* [ ] Expiry → re-login → resume

**Done when:**
You can delete cookies and still recover.

---

## 🌉 Day 4 — Browser → API Bridge

**Goal:** Scale without the browser.

**Checklist**

* [ ] Listen to responses
* [ ] Identify **real JSON endpoint**
* [ ] Capture:

  * [ ] Headers
  * [ ] Cookies
  * [ ] Tokens
* [ ] Replay request with `aiohttp`
* [ ] Fetch **10× pages** faster than browser

**Done when:**
Browser is used only for login/token capture.

---

## 🏗️ Day 5 — Production Minimum

**Goal:** Survive crashes & resume.

**Checklist**

* [ ] Folder structure exists
* [ ] Logs written with timestamps
* [ ] Checkpoint file saves progress
* [ ] Kill process mid-run
* [ ] Restart → resumes correctly
* [ ] Session expiry auto-handled

**Done when:**
You trust it to run unattended.

--