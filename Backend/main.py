from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
import random


# In-memory database for users
users = {
    "Alizy": {"pin": "1234", "balance": 50000},
    "Shahzaib": {"pin": "5678", "balance": 60000},
    "Aman": {"pin": "9876", "balance": 70000},
}

bank_balance = 50000

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request bodies
class AuthRequest(BaseModel):
    username: str
    password: str

class BankTransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float

class DepositRequest(BaseModel):
    username: str
    amount: float

class WithdrawRequest(BaseModel):
    username: str
    amount: float

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

# Authenticate endpoint
@app.post("/authenticate")
async def authenticate_user(request: AuthRequest):
    if request.username in users and users[request.username]["pin"] == request.password:
        return {"message": "Authentication successful", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Bank transfer endpoint
@app.post("/bank-transfer")
async def perform_bank_transfer(request: BankTransferRequest):
    sender_name = request.from_account
    receiver_name = request.to_account
    amount = request.amount

    # Validate amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")

    # Validate accounts
    if sender_name not in users:
        raise HTTPException(status_code=404, detail="Sender account not found.")
    if receiver_name not in users:
        raise HTTPException(status_code=404, detail="Receiver account not found.")
    if sender_name == receiver_name:
        raise HTTPException(status_code=400, detail="Sender and receiver accounts cannot be the same.")

    # Validate sender's balance
    if users[sender_name]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # Perform the transfer
    users[sender_name]["balance"] -= amount
    users[receiver_name]["balance"] += amount
    
    print(f"Transfer successful: {amount} from {sender_name} to {receiver_name}")
    
    return {
        "message": "Bank transfer successful",
        "transaction_id": f"txn_{random.randint(100000, 999999)}",
        "new_balance": users[sender_name]["balance"]
    }

# Deposit endpoint
@app.post("/deposit")
async def deposit_funds(request: DepositRequest):
    if request.username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    users[request.username]["balance"] += request.amount
    return {"message": "Deposit successful", "new_balance": users[request.username]["balance"]}

@app.get("/balance/{username}")
async def get_balance(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "balance": users[username]["balance"]}

# Withdraw endpoint
@app.post("/withdraw")
async def withdraw_funds(request: WithdrawRequest):
    if request.username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")

    if users[request.username]["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for withdrawal.")
    
    users[request.username]["balance"] -= request.amount
    return {"message": "Withdrawal successful", "new_balance": users[request.username]["balance"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
