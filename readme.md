# Product Catalog Microservice

This microservice is designed to manage a product catalog for an e-commerce platform. It provides advanced CRUD functionality and is built using Python, FastAPI, and MongoDB. For Demonstration Streamlit used.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+

## Installation

1 **Install dependencies**:

    pip install fastapi uvicorn pymongo python-dotenv streamlit requests

3. **Setup MongoDB**:
- Already MongoDB is running on MongoDB cluster on MongoDB Atlas.

4. **Environment Variables**:
- `.env` contain the database URI.

## Running the Application

To run the application, use the following command from the root directory of the project:

pip install fastapi uvicorn pymongo python-dotenv

    uvicorn app:app --reload
    
or

    uvicorn app:app --host 0.0.0.0 --port 80


## Funning Frontend

    streamlit run frontend.py

