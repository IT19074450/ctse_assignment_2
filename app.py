from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import ReturnDocument
from dotenv import load_dotenv
import os


app = FastAPI()

load_dotenv()
uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.products
product_collection = db.product

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    category: str

# Get the next product ID (auto-increment simulation)
def get_next_product_id():
    last_product = product_collection.find_one(sort=[("id", -1)])
    if last_product:
        return last_product['id'] + 1
    return 0

@app.get("/products", response_model=List[Product])
def list_products(category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = {}
    if category:
        query['category'] = category
    if min_price is not None:
        query['price'] = {'$gte': min_price}
    if max_price is not None:
        query['price'] = {'$lte': max_price}
    products = list(product_collection.find(query))
    return products

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    product = product_collection.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
def add_product(product: Product):
    product.id = get_next_product_id()
    product_collection.insert_one(product.model_dump())
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: Product):
    updated_product = product_collection.find_one_and_update(
        {"id": product_id},
        {"$set": product_update.model_dump(exclude_unset=True)},
        return_document=ReturnDocument.AFTER
    )
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    result = product_collection.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

@app.get("/search", response_model=List[Product])
def search_products(query: str):
    search_criteria = {"$regex": query, "$options": "i"}
    products = list(product_collection.find({"$or": [{"name": search_criteria}, {"description": search_criteria}]}))
    return products
