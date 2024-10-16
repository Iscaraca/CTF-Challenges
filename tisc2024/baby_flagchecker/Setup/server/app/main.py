# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connect_to_testnet import *

app = FastAPI()

class PasswordInput(BaseModel):
    password: str

@app.post("/check")
async def check(password_input: PasswordInput):
    password = password_input.password
    
    try:
        web3_client = connect_to_anvil()
        setup_contract = init_setup_contract(web3_client)
        output_json = call_check_password(setup_contract, password)

        return output_json
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))