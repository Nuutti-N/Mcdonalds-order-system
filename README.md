# Mcdonald-order-system 🍽️ 👨‍🍳 🍔 🍟

A simple order management system built with FastAPI and Python. 


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

5. Run the server  ( many ways) 
- uvicorn main:app --reload
- fastapi dev own file name.py

6. Open your Browser
- visit https://localhost:8000/docs

- You will see interactive API documentation!

## Built with
- FastAPI
- Pydantic
- SQLModel
- SQLite
  
## Database
This project uses SQLModel — a combination of SQLAlchemy and Pydantic, which makes it easier to work with databases in FastAPI.
Why a database instead of a list?
A list deletes all data when you stop the server. A database saves everything permanently — even if you close the app and come back later.

How it works:
engine — creates the connection to the database file

session — works like driving a car, it runs every time a change or update is made

commit — saves your changes permanently (like Ctrl+S)

## Refactor Files

## 📈 Project Status
- This project is actively being developed and improved daily.


## Little Tricks
- I made 11.3.2026, Little changes in project. Every router line I use with Session(engine) as session:, however you dont need to put everyline it, you need only one place.
- You have two choices, automatic or manual, even if you are beginner or intermediate, test both, therefore if someday you need some else. However I used in my project automatic version its little bit faster to use it, and you dont need close everytime it than manual version, because I know frequently everyone programmer forget small mistakes. 
  
## Contributing 🤝
- This is a learning project, but feedback is a welcome!

## 🔜 Next steps
- I will add comments to every line,so then you can understand what each lines does!










  
