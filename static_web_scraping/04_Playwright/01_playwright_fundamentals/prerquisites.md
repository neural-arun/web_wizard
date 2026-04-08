

# 🧠 PRE–DAY 0 CHECKLIST

*(You must understand these before touching Playwright or Scraping)*

---

## 1️⃣ What Is HTTP (Core Transport Layer)

You must understand:

* What is a request?
* What is a response?
* What is a URL?
* What is GET vs POST?
* What are headers?
* What is a status code (200, 404, 403, 429)?

If you don’t deeply understand this,
Network tab will look like random noise.

---

## 2️⃣ What Is HTML (Structure Layer)

You must understand:

* What is HTML?
* What is DOM?
* What is a tag?
* What is id/class?
* What is nested structure?
* What is CSS selector?

Without this:
You cannot reason about structure.

---

## 3️⃣ What Is JavaScript Doing on a Page

You must understand:

* JS can modify DOM after page loads.
* JS can call APIs in background.
* Page load ≠ data load.

If this is unclear,
you will always be confused about dynamic sites.

---

## 4️⃣ What Is XHR / Fetch

You must know:

* What is an API call?
* What is JSON?
* How browser fetches data in background.
* How to see that in Network tab.

This is critical for Day 0.

---

## 5️⃣ What Is GraphQL (High Level Only)

You must know:

* REST API returns fixed endpoints.
* GraphQL lets client ask for specific fields.
* GraphQL often uses POST with JSON body.
* Pagination is often cursor-based.

No need deep theory.
Just conceptual clarity.

---

## 6️⃣ What Is Pagination (System Thinking)

You must understand:

Server cannot send infinite data.

So it sends data in batches:

* page number
* offset
* cursor

You must conceptually understand this,
not just search for “page=2”.

---

## 7️⃣ How To Use Chrome DevTools Properly

You must be comfortable with:

* Elements tab
* Network tab
* Filtering by XHR
* Inspecting request payload
* Inspecting response JSON
* Comparing two requests

If you are slow here,
everything feels overwhelming.

---

# 🔥 Self-Test Before Day 0

If I ask you:

> What happens technically when you refresh a webpage?

You should be able to explain:

1. Browser sends HTTP request
2. Server responds with HTML
3. Browser builds DOM
4. JS runs
5. JS makes additional XHR/Fetch calls
6. Data injected into DOM

If you can’t explain that cleanly,
we must fix that first.

---
