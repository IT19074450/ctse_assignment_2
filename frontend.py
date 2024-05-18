import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Assuming the FastAPI app runs locally on port 8000

def list_products(category=None, min_price=None, max_price=None):
    params = {}
    if category:
        params['category'] = category
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    response = requests.get(f"{API_URL}/products", params=params)
    return response.json()

def add_product(name, description, price, category):
    product = {"name": name, "description": description, "price": price, "category": category}
    response = requests.post(f"{API_URL}/products", json=product)
    return response.json()

def update_product(product_id, name, description, price, category):
    product = {"name": name, "description": description, "price": price, "category": category}
    response = requests.put(f"{API_URL}/products/{product_id}", json=product)
    return response.json()

def delete_product(product_id):
    response = requests.delete(f"{API_URL}/products/{product_id}")
    return response.json()

def search_products(query):
    response = requests.get(f"{API_URL}/search", params={"query": query})
    return response.json()

# Streamlit UI
st.title("Product catelog microservice - Demo")

# List products
st.header("List Products")
category = st.text_input("Filter by category")
min_price = st.text_input("Minimum price")
max_price = st.text_input("Maximum price")
if st.button("List Products"):
    products = list_products(category, min_price, max_price)
    st.write(products)

# Add Product
st.header("Add a New Product")
with st.form(key='add_product_form'):
    name = st.text_input("Name")
    description = st.text_area("Description")
    price = st.number_input("Price", min_value=0.0)
    category = st.text_input("Category")
    submit_button = st.form_submit_button("Add Product")
    if submit_button:
        result = add_product(name, description, price, category)
        st.write(result)

# Update Product
st.header("Update Product")
product_id_update = st.text_input("Product ID to update")
with st.form(key='update_product_form'):
    name_update = st.text_input("New Name")
    description_update = st.text_area("New Description")
    price_update = st.number_input("New Price", min_value=0.0)
    category_update = st.text_input("New Category")
    update_button = st.form_submit_button("Update Product")
    if update_button:
        result = update_product(product_id_update, name_update, description_update, price_update, category_update)
        st.write(result)

# Delete Product
st.header("Delete Product")
product_id_delete = st.text_input("Product ID to delete")
if st.button("Delete Product"):
    result = delete_product(product_id_delete)
    st.write(result)

# Search Products
st.header("Search Products")
query = st.text_input("Search Query")
if st.button("Search"):
    results = search_products(query)
    st.write(results)
