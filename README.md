# Mcdonald-order-system 🍽️ 👨‍🍳 🍔 🍟

A simple order manaement system built with FastAPI and Python. 


## Features 
✅ Full CRUD API for order management
- Create orders (POST /order)
- View all orders (GET /orders)
- View single order (GET /order/{id})
- Update order status (PUT /order/{id}/status)
- Delete orders (DELETE /order/{id})
- Filter orders by status (GET /orders/pending, /orders/completed)
- Calculate total price (GET /order/total)

## API Endpoints


## 🚀 Getting Started 

### Requirements 

- Python 3.10+
- pip

# Installation 
- IMPORTANT: Always use virtual environment, never install globally!

1. Clone the repository:
-git clone
-then cd

4. Create virtual environment:
  - python/py -m venv .venv

3. Activate it:
  # Windows:
  .venv\Scripts\Activate
  # Mac/Linux
  source .venv\bin\activate

4. Install dependencies:
- pip install -r requirements.txt

 
# Run the server  ( many ways) 
- uvicorn main:app --reload
- fastapi dev own file name.py

## Built with
- FastAPI
- Pydantic

## 📈 Project Status
- This project is actively being developed and improved daily.

  
##contributing 🤝
- This is a learning project, but feedback is a welcome!

## Usage 
Visit http://localhost:8000/docs













  
