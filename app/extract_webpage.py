from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import html2text
import requests
from bs4 import BeautifulSoup

class URLRequest(BaseModel):
    url: str

router = APIRouter()

@router.post("/extract")
async def extract_text_from_url(request: URLRequest):
    """
    Receives a URL, sends a GET request to the URL, parses the HTML response,
    extracts the text, and returns the text.
    """
    try:
        response = requests.get(request.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text = text_maker.handle(soup.prettify())

        return {"text": text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))