import uvicorn
from app import createApp


app = createApp()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}
