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

    # hello

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

print("Page title:", soup.title.string)

# Example: Find fixture containers (adjust selector based on actual page structure)
fixtures = soup.select("div.gar-match-item")  # Change this if needed

print(f"Found {len(fixtures)} fixtures")

for f in fixtures[:5]:  # print first 5 fixtures
    print(f.get_text(separator=" | ", strip=True))

for f in fixtures[:5]:
    text = f.get_text(separator=" | ", strip=True)
    parts = text.split("|")
    print(parts)  # This will print out the split list so you can see the structure

    # This is just an example — adapt to the actual format
    print({
        "team_1": parts[0].strip(),
        "score_1": parts[1].strip(),
        "team_2": parts[-1].strip(),
        "venue": next((p.strip() for p in parts if "Venue:" in p), ""),
        "referee": next((p.strip() for p in parts if "Referee:" in p), ""),
    })

fixtures_data = []

for f in fixtures:
    parts = f.get_text(separator=" | ", strip=True).split("|")
    parts = [p.strip() for p in parts if p.strip()]  # clean empty strings

    try:
        team_1 = parts[0]
        goals_1 = parts[1]
        points_1 = parts[3]
        score_1 = f"{goals_1}-{points_1}"

        goals_2 = parts[4]
        points_2 = parts[6]
        score_2 = f"{goals_2}-{points_2}"

        team_2 = parts[-1]

        venue = next((p for p in parts if "Venue:" in p), "")
        referee = next((p for p in parts if "Referee:" in p), "")

        fixture = {
            "team_1": team_1,
            "score_1": score_1,
            "team_2": team_2,
            "score_2": score_2,
            "venue": venue,
            "referee": referee,
        }

        fixtures_data.append(fixture)

    except Exception as e:
        print("Skipping fixture due to unexpected format:", parts)



# Save JSON
import json
with open("website/fixtures.json", "w") as f:
    json.dump(fixtures_data, f, indent=2)


import json

# your scraping and parsing code here, then:

print(json.dumps(fixtures_data, indent=2))

import csv

keys = fixtures_data[0].keys()

with open('fixtures.csv', 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(fixtures_data)


