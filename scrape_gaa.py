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
# ... your playwright code above, up to parsing soup ...

fixtures_list = soup.find_all("div", class_="gar-match-item")

print(f"Found {len(fixtures_list)} fixtures")

# Preview the first few fixtures
for f in fixtures_list[:5]:
    print(f.get_text(separator=" | ", strip=True))

results = []
fixtures = []  # Initialize empty lists before use

for f in fixtures_list:
    text = f.get_text(separator=" | ", strip=True)
    parts = [p.strip() for p in text.split("|") if p.strip()]
    
    try:
        # Extract venue and referee by scanning parts
        venue = next((p for p in parts if p.startswith("Venue:")), "")
        referee = next((p for p in parts if p.startswith("Referee:")), "")
        
        # Remove venue and referee from parts to simplify
        parts_cleaned = [p for p in parts if not (p.startswith("Venue:") or p.startswith("Referee:"))]
        
        # The last item is team_2
        team_2 = parts_cleaned[-1]
        
        # The first item is team_1
        team_1 = parts_cleaned[0]
        
        # Find scores by looking for a pattern: number - number somewhere between team names
        # The scores should be consecutive parts: goals, "-", points for team 1 and team 2
        
        # We'll try to find first score pattern (team 1)
        score_1 = ""
        score_2 = ""
        for i in range(1, len(parts_cleaned)-1):
            if parts_cleaned[i] == '-' and i-1 >= 0 and i+1 < len(parts_cleaned):
                # Check if parts before and after '-' are digits
                if parts_cleaned[i-1].isdigit() and parts_cleaned[i+1].isdigit():
                    # First occurrence -> score_1
                    if not score_1:
                        score_1 = parts_cleaned[i-1] + "-" + parts_cleaned[i+1]
                    # Second occurrence -> score_2
                    elif not score_2:
                        score_2 = parts_cleaned[i-1] + "-" + parts_cleaned[i+1]
        
        fixture_data = {
            "team_1": team_1,
            "team_2": team_2,
            "venue": venue,
            "referee": referee,
        }
        if score_1 and score_2:
            fixture_data["score_1"] = score_1
            fixture_data["score_2"] = score_2
        
        # Decide results vs fixtures based on scores (or absence)
        if score_1 and score_2 and (score_1 != "0-0" or score_2 != "0-0"):
            results.append(fixture_data)
        else:
            fixtures.append(fixture_data)
    
    except Exception as e:
        print("Skipping fixture due to unexpected format:", parts, "| Error:", e)




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


