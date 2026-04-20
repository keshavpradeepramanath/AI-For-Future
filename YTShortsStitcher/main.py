from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import isodate

API_KEY = "YOUR_API_KEY"  # 🔴 PUT YOUR KEY HERE

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Get video details (duration + embeddable)
def get_video_details(video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "contentDetails,status",
        "id": ",".join(video_ids),
        "key": API_KEY
    }
    res = requests.get(url, params=params).json()
    return res.get("items", [])

# 🔹 Check if it's a Short (< 60 sec)
def is_short(duration):
    seconds = isodate.parse_duration(duration).total_seconds()
    return seconds <= 60

# 🔹 Search videos
def search_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 20,
        "type": "video",
        "videoEmbeddable": "true",  # 🔥 important
        "key": API_KEY
    }
    res = requests.get(url, params=params).json()
    return [item["id"]["videoId"] for item in res.get("items", [])]

@app.get("/playlist")
def get_playlist(
    category: str = Query("funny"),
    kids_safe: bool = Query(False)
):
    query = category + " short video vertical"

    if kids_safe:
        query = category + " kids educational short video"

    video_ids = search_videos(query)

    if not video_ids:
        return {"videos": []}

    details = get_video_details(video_ids)

    shorts = []

    for item in details:
        duration = item["contentDetails"]["duration"]
        embeddable = item["status"].get("embeddable", False)

        if embeddable and is_short(duration):
            shorts.append(item["id"])

    return {"videos": shorts}