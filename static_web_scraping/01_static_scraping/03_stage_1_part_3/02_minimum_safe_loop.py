"""
while True:
    html = self.fetch_html(current_url)

    if html is None:
        # page failed, but system alive
        break_or_continue = "continue"  # THINK: which one?
        continue

    soup = self.parse_html(html)
    self.extract_records(soup)

    next_button = soup.find("li", class_="next")
    if not next_button:
        break

    current_url = urljoin(current_url, next_button.find("a")["href"])

"""