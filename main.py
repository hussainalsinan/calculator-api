from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from google.cloud import bigquery

app = FastAPI()

def get_bq_client():
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Calculator API"}

@app.get("/add")
def add(a: float, b: float):
    return {"operation": "add", "a": a, "b": b, "result": a + b}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"operation": "subtract", "a": a, "b": b, "result": a - b}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"operation": "multiply", "a": a, "b": b, "result": a * b}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"operation": "divide", "a": a, "b": b, "result": a / b}

@app.get("/power")
def power(a: float, b: float):
    return {"operation": "power", "base": a, "exponent": b, "result": a ** b}

@app.get("/dbwritetest", status_code=200)
def dbwritetest(bq: bigquery.Client = Depends(get_bq_client)):
    row_to_insert = [
        {"endpoint": "/dbwritetest", "result": "Success", "status_code": 200}
    ]
    
    # Using your Project ID: project-89b435f7-0bc1-4282-819
    errors = bq.insert_rows_json("project-89b435f7-0bc1-4282-819.calculator.api_logs", row_to_insert)
    
    if errors:
        print(f"BigQuery Insert Errors: {errors}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Failed to log data to BigQuery", "errors": errors}
        )
    
    return {"message": "Log entry created successfully"}