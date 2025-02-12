from fastapi import FastAPI
from pydantic import BaseModel
from common.agent import monitoring_middleware
from common.update_consumer import start_update_consumer
import uvicorn

app = FastAPI(title="Payment Service")
app.middleware("http")(monitoring_middleware)

@app.on_event("startup")
async def startup_event():
    start_update_consumer()

class Payment(BaseModel):
    order_id: int
    amount: float

@app.post("/payment")
async def process_payment(payment: Payment):
    return {"order_id": payment.order_id, "status": "payment_successful", "amount": payment.amount}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
