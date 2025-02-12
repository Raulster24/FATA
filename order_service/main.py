from fastapi import FastAPI
from pydantic import BaseModel
from common.agent import monitoring_middleware
from common.update_consumer import start_update_consumer, current_threshold
import uvicorn
import asyncio

app = FastAPI(title="Order Service")
app.middleware("http")(monitoring_middleware)

@app.on_event("startup")
async def startup_event():
    start_update_consumer()
    print(f"Initial threshold is: {current_threshold}")

class Order(BaseModel):
    customer: str
    items: list[str]

@app.get("/order/{order_id}")
async def get_order(order_id: int):
    # Simulate a delay to trigger anomaly logging
    await asyncio.sleep(1.2)
    return {"order_id": order_id, "status": "processing", "items": ["item1", "item2"]}

@app.post("/order")
async def create_order(order: Order):
    return {"order_id": 123, "status": "created", "order": order.dict()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
