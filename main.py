from fastapi import FastAPI

from routes import client

app = FastAPI()


# Register routes
app.include_router(client.router)
