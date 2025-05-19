from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.gaa.ie/fixtures-results"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=False if you want to see the browser open
    page = browser.new_page()
    page.goto(url)

    # Wait for fixture elements to load, adjust selector as needed
    page.wait_for_selector("div.gar-matches-list")  

    html = page.content()
    browser.close()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

print("Page title:", soup.title.string)

# Example: Find fixture containers (adjust selector based on actual page structure)
fixtures = soup.select("div.gar-match-item")  # Change this if needed

print(f"Found {len(fixtures)} fixtures")

for f in fixtures[:5]:  # print first 5 fixtures
    print(f.get_text(separator=" | ", strip=True))