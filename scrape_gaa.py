from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

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
# ... your playwright code above, up to parsing soup ...

fixtures_list = soup.find_all("div", class_="gar-match-item")

print(f"Found {len(fixtures_list)} fixtures")

# Preview the first few fixtures
for f in fixtures_list[:5]:
    print(f.get_text(separator=" | ", strip=True))

results = []
fixtures = []

for f in fixtures_list:
    # Infer game from the match link URL
    link = f.find("a", href=True)
    href = link["href"] if link else ""
    if "/hurling/" in href:
        game = "hurling"
    elif "/football/" in href:
        game = "football"
    else:
        game = "unknown"

    # Optionally skip non-senior games
    if "senior" not in href:
        continue

    date_heading = f.find_previous("h2", class_="gar-matches-list__date")
    raw_date = date_heading.get_text(strip=True) if date_heading else ""
    try:
        date_obj = datetime.strptime(f"{raw_date} {datetime.now().year}", "%A %d %B %Y")
        iso_date = date_obj.isoformat()
    except:
        iso_date = ""


    # Now parse the rest of the fixture
    text = f.get_text(separator=" | ", strip=True)
    parts = [p.strip() for p in text.split("|") if p.strip()]

    venue = next((p for p in parts if p.startswith("Venue:")), "")
    referee = next((p for p in parts if p.startswith("Referee:")), "")

    parts_cleaned = [p for p in parts if not (p.startswith("Venue:") or p.startswith("Referee:"))]
    team_1 = parts_cleaned[0]
    team_2 = parts_cleaned[-1]

    # Find goal–point patterns
    score_1 = score_2 = ""
    for i in range(1, len(parts_cleaned) - 1):
        if parts_cleaned[i] == "-" and parts_cleaned[i-1].isdigit() and parts_cleaned[i+1].isdigit():
            if not score_1:
                score_1 = f"{parts_cleaned[i-1]}-{parts_cleaned[i+1]}"
            elif not score_2:
                score_2 = f"{parts_cleaned[i-1]}-{parts_cleaned[i+1]}"

    fixture_data = {
        "team_1": team_1,
        "team_2": team_2,
        "venue": venue,
        "referee": referee,
        "game": game,
        "url": href,
        "date": iso_date      # ← newly added field
    }

    if score_1 and score_2 and (score_1 != "0-0" or score_2 != "0-0"):
        fixture_data["score_1"] = score_1
        fixture_data["score_2"] = score_2
        results.append(fixture_data)
    else:
        fixtures.append(fixture_data)






# Save JSON
# Save JSON
import json
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

with open("fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)




import json

# your scraping and parsing code here, then:

print("Results:\n", json.dumps(results, indent=2))
print("Fixtures:\n", json.dumps(fixtures, indent=2))

import csv

if results:  # check if not empty
    keys = results[0].keys()
    with open('results.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

if fixtures:  # check if not empty
    keys = fixtures[0].keys()
    with open('fixtures.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(fixtures)


