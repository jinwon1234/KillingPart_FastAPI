import yt_dlp
from models import SearchRequest
import re


def normalize(query: str):
    if not query:
        return ""
    query = query.replace("#", " ")
    query = re.sub(r"[(){}\[\]]", " ", query)
    query = re.sub(r"[^0-9a-zA-Z가-힣 ]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()
    return query

def priority(title: str) -> int:
    t = title.lower() 
    
    if "official audio" in t:
        return 1

    if "lyric video" in t or "lyrics" in t or "가사" in t:
        return 2

    if ("official music video" in t
        or "official video" in t
        or "official mv" in t):
        return 3
    
    if "official visualizer" in t:
        return 4

    return 5


def search(req: SearchRequest):

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
        artist = normalize(req.artist)
        title = normalize(req.title)

        combined_query = f"{artist} {title}".strip()

        search_result = ydl.extract_info(f"ytsearch5:{combined_query}", download=False)

        entries = [
            {
                "id": e.get("id"),
                "title": e.get("title"),
                "duration": e.get("duration")
            }
            for e in search_result.get("entries", [])
            if e.get("id")
        ]

        entries.sort(key=lambda e: priority(e["title"] or ""))

        return entries