from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom handler to return the exact "friendly" error message required by the assignment
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "All arguments must be valid numbers."},
    )

@app.get("/")
def health_check():
    """Returns a simple health status to verify the API is running."""
    return {"status": "healthy"}

@app.get("/add/{a}/{b}")
def add(a: float, b: float):
    """Adds two numbers and returns the operation details."""
    return {"operation": "add", "a": a, "b": b, "result": a + b}

@app.get("/subtract/{a}/{b}")
def subtract(a: float, b: float):
    """Subtracts b from a and returns the operation details."""
    return {"operation": "subtract", "a": a, "b": b, "result": a - b}

@app.get("/multiply/{a}/{b}")
def multiply(a: float, b: float):
    """Multiplies two numbers and returns the operation details."""
    return {"operation": "multiply", "a": a, "b": b, "result": a * b}

@app.get("/divide/{a}/{b}")
def divide(a: float, b: float):
    """Divides a by b. Returns a 422 error if b is zero."""
    if b == 0:
        raise HTTPException(
            status_code=422,
            detail="Division by zero is not allowed."
        )
    return {"operation": "divide", "a": a, "b": b, "result": a / b}

# CUSTOM ENDPOINTS

@app.get("/average/{a}/{b}/{c}")
def average(a: float, b: float, c: float):
    """Calculates the average of three numbers."""
    result = (a + b + c) / 3
    return {"operation": "average", "a": a, "b": b, "c": c, "result": result}

@app.get("/square/{a}")
def square(a: float):
    """Calculates the square of a number."""
    return {"operation": "square", "a": a, "result": a ** 2}

@app.get("/power/{a}/{b}")
def power(a: float, b: float):
    """Calculates a raised to the power of b."""
    return {"operation": "power", "base": a, "exponent": b, "result": a ** b}