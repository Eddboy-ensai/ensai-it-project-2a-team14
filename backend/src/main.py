from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from controller import user_controller
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VeloScope")

app.include_router(user_controller.router, prefix="/user", tags=["Users"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=int(os.getenv("UVICORN_PORT", "5000")),
    )