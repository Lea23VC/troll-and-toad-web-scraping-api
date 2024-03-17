from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.scraping import scrap_toad_and_toad


router = APIRouter()


@router.get("/", response_model=List[str])
async def search(name: str):
    results = scrap_toad_and_toad(name)
    return JSONResponse(content=results)
