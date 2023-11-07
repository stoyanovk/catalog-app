from db.db import init_models
import asyncio


def db_init_models():
    asyncio.run(init_models())
    print("Done")


db_init_models()
