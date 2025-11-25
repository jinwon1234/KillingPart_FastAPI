from fastapi import FastAPI
from models import SearchRequest
import youtube_search

app = FastAPI()

@app.post("/api/youtube/search")
def get_youtube_info(req: SearchRequest):
    return youtube_search.search(req)