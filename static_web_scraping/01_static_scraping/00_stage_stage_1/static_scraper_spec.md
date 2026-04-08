# 📄 UNIVERSAL STATIC WEBSITE SCRAPER SPEC
## (Fill this → Give to AI → Get Production-Ready Scraper)

---

## 🔹 SECTION 1: WEBSITE BASICS

WEBSITE_NAME:
WEBSITE_URL (base / start page):

IS_WEBSITE_STATIC (yes / no):
How confirmed?
(e.g. data visible in page HTML, no XHR / fetch calls)

---

## 🔹 SECTION 2: REQUEST / IDENTITY (HEADERS)

NEEDS_HEADERS (yes / no):

If YES, fill below:
User-Agent:
Accept-Language:
Other headers (if any):

Does the site block requests without headers? (yes / no)

---

## 🔹 SECTION 3: RECORD IDENTIFICATION (MOST IMPORTANT)

WHAT IS ONE RECORD?
(e.g. one product / one book / one quote)

PARENT_TAG:
PARENT_CLASS or ID:

How did you confirm this parent?
(e.g. hover highlights full record, repeats on page)

---

## 🔹 SECTION 4: DATA FIELDS TO EXTRACT

### FIELD 1
FIELD_NAME:
TAG:
CLASS / ID:
IS_TEXT_OR_ATTRIBUTE (text / attribute):
If attribute → ATTRIBUTE_NAME:
Any cleaning needed?
(e.g. strip, replace, lowercase, mapping)

---

### FIELD 2
FIELD_NAME:
TAG:
CLASS / ID:
IS_TEXT_OR_ATTRIBUTE (text / attribute):
If attribute → ATTRIBUTE_NAME:
Any cleaning needed?

---

### FIELD 3
FIELD_NAME:
TAG:
CLASS / ID:
IS_TEXT_OR_ATTRIBUTE (text / attribute):
If attribute → ATTRIBUTE_NAME:
Any cleaning needed?

---

(Add more fields as required)

---

## 🔹 SECTION 5: SPECIAL DATA LOGIC (IMPORTANT)

Is any data encoded inside class names? (yes / no)

If YES:
- FIELD_NAME:
- Example class list (as seen in HTML):
- How to extract actual value:
(e.g. last class name, mapping text to number)

Is any field sometimes missing? (yes / no)
If YES, which field(s):

---

## 🔹 SECTION 6: PAGINATION / FLOW

IS_PAGINATION_PRESENT (yes / no):

If YES:
NEXT_BUTTON_TAG:
NEXT_BUTTON_CLASS:

LINK_TYPE (relative / absolute):

EXAMPLE_NEXT_LINK (from HTML):
(e.g. page-2.html)

STOP_CONDITION:
(e.g. next button missing / disabled)

---

## 🔹 SECTION 7: OUTPUT REQUIREMENTS

OUTPUT_FORMAT (json / csv / print only):

FILE_NAME (if saving to file):

Should data be returned as list of dictionaries? (yes / no)

---

## 🔹 SECTION 8: ENGINEERING PREFERENCES

USE_SCRAPER_CLASS (yes / no): yes

EXPECTED_METHODS:
(fetch_html, parse_html, extract_records, paginate, save_output)

USE_TYPE_HINTS (yes / no):
USE_PYDANTIC (yes / no):

ERROR_HANDLING_LEVEL:
(basic / safe-skip / strict-fail)

Any performance concerns?
(low / medium / high)

---

## 🔹 SECTION 9: FINAL INSTRUCTION TO AI (DO NOT EDIT)

TASK FOR AI:

Using the above specification, generate a clean, 
production-quality Python scraper for a STATIC website.

Requirements:
- Use requests + BeautifulSoup
- Use a Scraper class
- Follow separation of concerns:
  network / parser / extractor / flow / output
- Handle missing data safely
- Do NOT over-engineer
- Add clear comments explaining logic
