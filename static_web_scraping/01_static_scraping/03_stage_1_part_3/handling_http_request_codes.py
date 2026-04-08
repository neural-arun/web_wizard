import requests

def fetch_html(self, url):
    try:
        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code == 200:
            return response.text

        elif response.status_code == 404:
            print(f"[404] Page not found: {url}")# print is for the debugging and human feedback

            return None # return is for the program.

        elif response.status_code == 403:
            print(f"[403] Blocked by server: {url}")
            return None

        elif response.status_code == 429:
            print(f"[429] Too many requests: {url}")
            return None

        else:
            print(f"[{response.status_code}] Unexpected error")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network issue: {e}")
        return None

