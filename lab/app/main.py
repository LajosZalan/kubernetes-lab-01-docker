from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Subscription Tracker")

subscriptions = {}

class Subscription(BaseModel):
    # name: str | None = None
    price: float = 0
    billing_cycle: str | None = None


@app.get("/")
def root():
    return {
        "message": "Subscription Tracker API"
    }


@app.post("/subscriptions")
def create_subscription(name: str, subscription: Subscription):
    # name = subscription.name
    if name in subscriptions:
        raise HTTPException(status_code=409, detail="Subscription already exists")

    subscriptions[name] = subscription.model_dump()

    return {
        "name": name,
        **subscriptions[name]
    }


@app.get("/subscriptions")
def get_subscriptions():
    return subscriptions


@app.get("/subscriptions/{name}")
def get_subscription(name: str):
    if name not in subscriptions:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return {
        "name": name,
        **subscriptions[name]
    }

@app.delete("/subscriptions/{name}")
def delete_subscription(name: str):
    if name not in subscriptions:
        raise HTTPException(status_code=404, detail="Subscription not found")

    del subscriptions[name]

    return {
        "message": f"{name} deleted"
    }


@app.get("/summary")
def get_summary():
    monthly_cost = 0

    for subscription in subscriptions.values():
        if subscription["billing_cycle"] == "monthly":
            monthly_cost += subscription["price"]

        elif subscription["billing_cycle"] == "yearly":
            monthly_cost += subscription["price"] / 12

    return {
        "subscriptions": len(subscriptions),
        "monthly_cost": round(monthly_cost, 2),
        "yearly_cost": round(monthly_cost * 12, 2)
    }
