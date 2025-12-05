from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

data = [
    {'id': 1, 'name': 'iphone17', 'price': 100},
    {'id': 2, 'name': 'iphone18', 'price': 100},
]


# GEt Request
# Read or Fetch ALL DAta
@app.get('/')
def home():
    ''' home '''
    return {"message": "Hello World"}


@app.get('/product')
async def all_products():
    ''' home '''
    return {"response": data}


# Read or fetch single product
@app.get("/product/{product_id}")
async def single_product(product_id: int):
    ''' get single product '''
    product = next((item for item in data if item["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"response": product}


# POST Request
# Create or Insert Data
@app.post("/product")
async def create_product(new_product: dict):
    ''' create product '''
    data.append(new_product)
    return {"response": new_product}


# PUT Request
# Update Complete Data
@app.post("/product/{product_id}")
async def update_product(product_id: int, updated_product: dict):
    ''' create product '''
    index = next((i for i, item in enumerate(data) if item["id"] == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # replace the whole object
    data[index] = updated_product
    return {"response": updated_product}


# Partial update
@app.patch("/product/{product_id}")
async def patch_product(product_id: int, partial_data: dict):
    """Partial update for product"""
    product = next((item for item in data if item["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # update only given keys
    for key, value in partial_data.items():
        product[key] = value

    return {"response": product}


# Delete resource
@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    """Delete a product"""
    index = next((i for i, item in enumerate(data) if item["id"] == product_id), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted = data.pop(index)

    return {"message": "Product deleted", "deleted": deleted}




# Parameter with types
@app.get("/get-product/{product_id}")
async def retrieve_product(product_id: int):
    ''' single product '''
    product = next((item for item in data if item["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"response": product}


# parameter order
@app.get("/product-title/rode_nt_usb")
async def get_product_by_hard_coded_title():
    ''' get product by title '''
    return {"response": "get_product_by_hard_coded_title"}


@app.get("/product-title/{product_title}")
async def get_product_by_title(product_title: str):
    ''' get product by title'''
    return {"response": "Single Data Fetched", "product_title": product_title}


# @app.get("/product-title/rode_nt_usb")
# async def get_product_by_hard_coded_title():
#     ''' get product by title, it will not execute because path match get_product_by_title '''
#     return {"response": "Single Data Fetched"}


# path parameter pre define value
class ProductCategory(str, Enum):
    ''' category enum class '''
    books = "books"
    clothing = "clothing"
    electronics = "electronics"


@app.get("/product/category/{category}")
async def get_product_by_category(category: ProductCategory):
    ''' get product by category '''
    # return {"response": "Product fetched by category", "category": category}
    if category == ProductCategory.books:
        return {"category": category, "message": "Books are awesome!"}
    elif category == ProductCategory.clothing:
        return {"category": category, "message": "Clothing are awesome!"}
    else:
        return {"category": category, "message": "Unknown category"}


# path converter
@app.get("/files/{file_path:path}")  # when need full path capture
async def read_file(file_path: str):
    ''' file path '''
    return {"message": "you requested file at path", "file": file_path}


# single query parameter
# http://127.0.0.1:8000/single-product?category=book&limit=5
# @app.get("/single-product")
# async def single_query_parameter(category: str):
#     ''' single query parameter '''
#     return {"status": "ok", "category": category}

# multiple query params
# @app.get("/single-product")
# async def single_query_parameter(limit: int, category: str):
#     ''' single query parameter '''
#     return {"status": "ok", "category": category, "limit": limit}

# default value and optional query params
# @app.get("/single-product")
# async def single_query_parameter(limit: int = 10, category: str = None):
#     ''' single query parameter '''
#     return {"status": "ok", "category": category, "limit": limit}


# path and query parameter
# http://127.0.0.1:8000/single-product/2025?category=book
@app.get("/single-product/{year}")
async def single_query_parameter(year: str, category: str):
    ''' single query parameter '''
    return {"status": "ok", "year": year, "category": category}
