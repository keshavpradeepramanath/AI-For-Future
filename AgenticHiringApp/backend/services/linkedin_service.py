import requests
from bs4 import BeautifulSoup
import urllib.parse
import time


def find_linkedin_profile(name, role):
    """
    Search Google for a LinkedIn profile using name + role.

    Returns:
        LinkedIn profile URL (str) OR None
    """

    try:
        # ✅ Build smart query
        query = f'site:linkedin.com/in "{name}" "{role}"'
        encoded_query = urllib.parse.quote(query)

        url = f"https://www.google.com/search?q={encoded_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }

        print(f"🔍 Searching LinkedIn for: {name} | Role: {role}")

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"❌ Google request failed: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ Extract LinkedIn URLs
        for link in soup.select("a"):
            href = link.get("href")

            if not href:
                continue

            if "/url?q=" in href:
                clean_url = href.split("/url?q=")[1].split("&")[0]

                if "linkedin.com/in" in clean_url:
                    print(f"✅ Found LinkedIn: {clean_url}")
                    return clean_url

        print("⚠️ No LinkedIn profile found")
        return None

    except Exception as e:
        print("❌ LinkedIn search error:", str(e))
        return None


# 🔥 OPTIONAL: safer version with fallback queries
def find_linkedin_profile_advanced(name, role):
    """
    Tries multiple queries for better accuracy.
    """

    queries = [
        f'site:linkedin.com/in "{name}" "{role}"',
        f'site:linkedin.com/in "{name}"',
        f'{name} linkedin {role}'
    ]

    for q in queries:
        try:
            encoded_query = urllib.parse.quote(q)
            url = f"https://www.google.com/search?q={encoded_query}"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            print(f"🔍 Trying query: {q}")

            response = requests.get(url, headers=headers, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.select("a"):
                href = link.get("href")

                if href and "/url?q=" in href:
                    clean_url = href.split("/url?q=")[1].split("&")[0]

                    if "linkedin.com/in" in clean_url:
                        print(f"✅ Found LinkedIn: {clean_url}")
                        return clean_url

            time.sleep(1)  # prevent blocking

        except Exception as e:
            print("❌ Error in advanced search:", str(e))

    print("⚠️ No LinkedIn profile found after multiple attempts")
    return None