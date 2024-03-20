from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from utils.scraping import scrap_toad_and_toad

from enums.Category import Category
from fastapi.responses import JSONResponse
from utils.scraping import scrap_toad_and_toad


router = APIRouter()


# Dependency to validate and convert category
def validate_category(category: str = Path(..., description="The category of the item")):
    category_enum = Category.get(category)
    if not category_enum:
        raise HTTPException(
            status_code=400, detail=f"Invalid category: {category}. Available categories: {[c.name for c in Category]}")
    return category_enum.value


@router.get("/", response_model=List[str])
async def search(name: str):
    results = scrap_toad_and_toad(name)
    if not results:  # Check if the results list is empty
        raise HTTPException(status_code=404, detail="No results found")
    return JSONResponse(content=results)


@router.get("/{category}/", response_model=List[str])
async def search(name: str, category: str = Depends(validate_category)):
    results = scrap_toad_and_toad(name, category)
    if not results:  # Check if the results list is empty
        raise HTTPException(status_code=404, detail="No results found")
    return JSONResponse(content=results)
