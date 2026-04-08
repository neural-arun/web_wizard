

# 🧠 PART 1 — TUMHARE SCRIPT KA STRUCTURAL BREAKDOWN

Think of scraper as **PIPELINE**, not code.

---

## 🔹 STEP 0: Imports (TOOLS LAYER)

```python
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from urllib.parse import urljoin
```

### WHAT

External tools jo scraper ko power dete hain

### WHY

* `requests` → website se HTML laane ke liye
* `BeautifulSoup` → HTML todne ke liye
* `json` → data store karne ke liye
* `Path` → file paths safe banane ke liye
* `urljoin` → pagination ke URLs safely jodne ke liye

🧠 **Rule**:

> Imports = capabilities of your scraper

---

## 🔹 STEP 1: Scraper Class (CONTAINER)

```python
class BooksScraper:
```

### WHAT

Scraper ek **machine** hai → class uska body

### WHY

* Reusability
* Clean design
* Multiple websites scrape kar sakte ho

🧠 **Rule**:

> 1 website / 1 scraper class

---

## 🔹 STEP 2: `__init__` (CONFIGURATION ZONE)

```python
def __init__(self, base_url):
```

### WHAT

Initial settings

### WHY

Ye cheezein har method ko chahiye:

* base URL
* headers
* data container

```python
self.base_url = base_url
self.headers = {...}
self.book_data = []
```

🧠 **Rule**:

> `__init__` = permanent memory of scraper

---

## 🔹 STEP 3: fetch_html() (NETWORK LAYER)

```python
def fetch_html(self, url):
```

### WHAT

Website se raw HTML laata hai

### WHY

* Network logic alag rakho
* Future mein retry / timeout / proxy add kar sakte ho

🧠 **Rule**:

> Never mix fetching + parsing

---

## 🔹 STEP 4: parse_html() (PARSING LAYER)

```python
def parse_html(self, html):
```

### WHAT

HTML → BeautifulSoup object

### WHY

* Separation of concerns
* Testing easy hota hai

🧠 **Rule**:

> HTML string ≠ DOM object

---

## 🔹 STEP 5: extract_records() (DATA EXTRACTION CORE)

```python
def extract_records(self, soup):
```

### WHAT

Ek page ke **saare records** extract karta hai

### WHY

* Website-specific logic yahin hota hai
* Baaki scraper generic rehta hai

Inside:

```python
records = soup.find_all(...)
for record in records:
    ...
    self.book_data.append(data)
```

🧠 **Rule**:

> 1 record → 1 dict

---

## 🔹 STEP 6: extract_all_pages() (PAGINATION ENGINE)

```python
def extract_all_pages(self):
```

### WHAT

Pages ko tab tak scrape karta hai jab tak `next` exist karta hai

### FLOW:

```text
current_url
↓
fetch
↓
parse
↓
extract records
↓
find next
↓
repeat / stop
```

Critical lines:

```python
next_button = soup.find("li", class_="next")
if not next_button:
    break
```

🧠 **Rule**:

> Pagination = loop + stop condition

---

## 🔹 STEP 7: save_to_json() (OUTPUT LAYER)

```python
def save_to_json(self):
```

### WHAT

Scraped data ko persist karta hai

### WHY

* Scraping ≠ storage
* Future mein CSV / DB add kar sakte ho

🧠 **Rule**:

> Storage logic always separate

---

## 🔹 STEP 8: main block (EXECUTION ZONE)

```python
if __name__ == "__main__":
```

### WHAT

Scraper ko run karta hai

### WHY

* Module reusable ban jaata hai
* Import safe hota hai

🧠 **Rule**:

> Class ≠ execution

---

# 🧠 PART 2 — GENERAL STATIC WEBSITE SCRAPER SKELETON

🔥 **THIS IS WHAT YOU SAVE FOREVER**

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0",
        }
        self.data = []

    # 1️⃣ FETCH
    def fetch_html(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    # 2️⃣ PARSE
    def parse_html(self, html):
        return BeautifulSoup(html, "lxml")

    # 3️⃣ EXTRACT RECORDS (WEBSITE-SPECIFIC)
    def extract_records(self, soup):
        raise NotImplementedError("Define record extraction logic")

    # 4️⃣ FIND NEXT PAGE (WEBSITE-SPECIFIC)
    def get_next_page(self, soup, current_url):
        raise NotImplementedError("Define pagination logic")

    # 5️⃣ MAIN LOOP
    def scrape_all(self):
        current_url = self.base_url

        while current_url:
            html = self.fetch_html(current_url)
            soup = self.parse_html(html)

            self.extract_records(soup)
            current_url = self.get_next_page(soup, current_url)
```

---

## 🔹 HOW YOU REDESIGN FOR ANY WEBSITE

Only override **2 methods** 👇

```python
def extract_records(self, soup):
    pass

def get_next_page(self, soup, current_url):
    pass
```

बाकी सब **SAME रहेगा** 🔥

---

## 🧠 MENTAL TEMPLATE (REMEMBER THIS)

```text
CONFIG
↓
FETCH
↓
PARSE
↓
EXTRACT
↓
PAGINATE
↓
STORE
```

---

