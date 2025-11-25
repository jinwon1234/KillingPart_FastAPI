from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    title:str = Field(..., min_length=1)  
    artist:str = Field(..., min_length=1)  