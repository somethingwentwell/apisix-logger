from typing import Any
from fastapi import Body, FastAPI


app = FastAPI()


@app.post("/logs")
async def log_handler(log_data: Any = Body(None)):
    print(log_data)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
