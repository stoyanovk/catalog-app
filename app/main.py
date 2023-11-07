from fastapi import FastAPI
from api.user.route import user_router


app = FastAPI()

app.include_router(user_router, prefix="/api")
