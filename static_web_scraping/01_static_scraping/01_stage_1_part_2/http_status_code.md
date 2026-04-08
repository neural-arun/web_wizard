

# 🧠 HTTP STATUS CODES — ENGINEER VERSION (HINGLISH)

## 🔑 Core Idea (1 line)

**HTTP status code = server ka short reply**
“Request samajh aayi, kaam hua ya nahi — aur kyun?”

Socho tum Swiggy order kar rahe ho 🍔
Status code = delivery app ka reply.

---

## 🟢 2xx — SUCCESS (Kaam ho gaya)

### **200 OK**

* Matlab: “Request sahi, data mil gaya”
* Scraping me: **HTML mil gaya**

📦 Analogy:

> Order diya → food mil gaya

⚠️ Engineer Note:

* 200 aane ka matlab **data correct hai** — ye assume mat karo
* Kabhi 200 ke saath **fake / empty HTML** bhi hota hai (advanced topic later)

---

### **201 Created**

* Mostly APIs me
* Matlab: “Naya data create ho gaya”

📦 Example:

* POST request → naya user ban gaya

Scraping me rare hai, but backend me common.

---

## 🔵 3xx — REDIRECTION (Rasta badal diya)

### **301 / 302**

* Matlab: “Page yahan nahi, wahan jao”

📦 Analogy:

> Restaurant band → next branch pe bhej diya

Scraping me:

* Old URL → new URL
* `requests` default handle kar leta hai

⚠️ Engineer Question:

* Agar redirect loop ho gaya toh?

---

## 🟡 4xx — CLIENT ERROR (Tumhari galti)

### **404 Not Found**

* Matlab: “Yeh page exist hi nahi karta”

📦 Analogy:

> Ghar ka address galat

Scraping cause:

* Pagination URL wrong
* Category removed

🛠 Action:

* Stop scraping that URL
* Log error

---

### **403 Forbidden** ⚠️⚠️⚠️

* Matlab: “Samajh gaya, par allow nahi”

📦 Analogy:

> Guard bolta: “Entry nahi milegi”

Scraping cause:

* Bot detect ho gaya
* Missing / bad headers

🛠 Engineer response:

* Headers improve
* Slow down
* Accept you’re blocked

❌ Galti beginners ki:

> “Code galat hai”
> No. **System ne mana kiya.**

---

### **429 Too Many Requests** 🔥

* Matlab: “Bohot fast aa rahe ho”

📦 Analogy:

> Ek hi aadmi 100 baar gate knock kare

Scraping cause:

* No rate limiting
* Too many requests

🛠 Engineer fix:

* Sleep
* Retry later
* Async me semaphore (later)

---

## 🔴 5xx — SERVER ERROR (Unki galti)

### **500 Internal Server Error**

* Matlab: “Server toot gaya”

📦 Analogy:

> Kitchen me gas khatam

Scraping mindset:

* Tum kuch nahi kar sakte
* Retry later
* Log and skip

---

### **502 / 503**

* Server overload / maintenance

🧠 Engineer rule:

> 5xx = retry + patience

---

## 🧠 SUMMARY TABLE (MEMORY ANCHOR)

| Code    | Meaning     | Scraper Action |
| ------- | ----------- | -------------- |
| 200     | OK          | Parse data     |
| 301/302 | Redirect    | Follow URL     |
| 403     | Blocked     | Headers / slow |
| 404     | Not found   | Skip URL       |
| 429     | Too fast    | Rate limit     |
| 500+    | Server down | Retry later    |

---
