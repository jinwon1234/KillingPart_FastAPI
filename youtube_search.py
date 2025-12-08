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

def priority(title: str, artist: str) -> int:

    if "official audio" in title:
        base = 1
    elif "lyric video" in title or "lyrics" in title or "가사" in title:
        base = 2
    elif ("official music video" in title
          or "official video" in title
          or "official mv" in title):
        base = 3
    elif "official visualizer" in title:
        base = 4
    else:
        base = 5

    if not artist:  
        base += 10   

    return base


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

        search_result = ydl.extract_info(f"ytsearch20:{combined_query}", download=False)

        entries = [
            {
                "id": e.get("id"),
                "title": e.get("title"),
                "duration": e.get("duration")
            }
            for e in search_result.get("entries", [])
            if e.get("id")
        ]

        entries.sort(key=lambda e: priority(e["title"] or "", artist))

        return entries[:5]