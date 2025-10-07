
import requests

API_KEY = "AIzaSyDAjGKxAF5288FSdBX3NIlidJ6G6RYZ784"
endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

params = {
    "query": "Suger cause diabetes",  # your search text
    "languageCode": "en",
          # only results from last year
    "pageSize": 10,
    # "reviewPublisherSiteFilter": "reuters.com",  # optional
}

try:
    resp = requests.get(endpoint, params={**params, "key": API_KEY})
    resp.raise_for_status()
    data = resp.json()
    if not data.get("claims"):
        print("No claims found in the response. Full response:")
        print(data)
    else:
        for c in data.get("claims", []):
            print("Claim:", c.get("text"))
            print("Claimant:", c.get("claimant"))
            print("Claim date:", c.get("claimDate"))
            for r in c.get("claimReview", []):
                print("  Publisher:", r["publisher"]["name"], "-", r.get("url"))
                print("  Rating:", r.get("textualRating"))
            print("-" * 60)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)

# Pagination: if present, repeat request with pageToken=data.get("nextPageToken")