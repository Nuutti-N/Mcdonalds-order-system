
from fastapi import FastAPI
from users import router as users_router
from routers import router as orders_router

# Here we make variables (app) and we import FastAPI from the fastapi library, so we put FastAPI().
app = FastAPI()
app.include_router(users_router)
app.include_router(orders_router)


@app.get("/Goodbye", tags=["Welcome"])
# asyn def allos handling multiple request simultaneously without waiting.
async def welcome_back():
    # Return message.
    return {"Message": "Thank you for visiting, and welcome back."}
