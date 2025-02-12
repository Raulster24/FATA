from fastapi import FastAPI
from common.agent import monitoring_middleware
from common.update_consumer import start_update_consumer
import uvicorn

app = FastAPI(title="Inventory Service")
app.middleware("http")(monitoring_middleware)

@app.on_event("startup")
async def startup_event():
    start_update_consumer()

@app.get("/inventory/{item_id}")
async def get_inventory(item_id: str):
    return {"item_id": item_id, "stock": 50}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
