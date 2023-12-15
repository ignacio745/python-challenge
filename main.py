from fastapi import FastAPI
from database.database import Base, engine
from routers.bookings import booking_router
from routers.users import user_router
from routers.auth import auth_router
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(booking_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)