from typing import List

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/", response_model=List[str])
async def search(query: str):
    return ["item1", "item2"]
