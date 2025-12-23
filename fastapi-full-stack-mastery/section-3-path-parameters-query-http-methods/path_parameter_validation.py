# response status code
from ast import alias
from typing import Annotated
from fastapi import FastAPI, Path, Query, status, HTTPException
from pydantic import AfterValidator


app = FastAPI()

products = [
    {
        "id": 1,
        "title": "Ravan Backpack",
        "price": 109.95,
        "description": "Perfect for everyday use and forest walks."
    },
    {
        "id": 2,
        "title": "Slim Fit T-Shirts",
        "price": 22.3,
        "description": "Comfortable, slim-fitting casual shirts."
    },
    {
        "id": 3,
        "title": "Cotton Jacket",
        "price": 55.99,
        "description": "Great for outdoor activities and gifting."
    }
]


# Basic path parameter
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found."
    )


# Path parameter Numeric validation with annotated
@app.get("/products/single/{product_id}")
async def get_single_product(product_id: Annotated[int, Path(ge=1, le=3)]):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found."
    )


# Adding meta data to path parameter
@app.get("/products/single/meta-data/{product_id}")
async def get_single_product_meta_data(
    product_id: Annotated[
        int,
        Path(
            title="The ID of the product to get",
            description="Must be between 1 and 3",
        )
    ]
):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found."
    )


# Combine path and query parameters
@app.get("/products/combine/{product_id}")
async def get_combine_product_meta_data(
    product_id: Annotated[int, Path(gt=0, le=100)],
    search: Annotated[str | None, Query(max_length=20)] = None
):
    for product in products:
        if product["id"] == product_id:
            if search and search.lower() not in product["title"].lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {product_id} not found for search '{search}'."
                )
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found."
    )
