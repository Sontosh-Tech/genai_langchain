from fastapi import FastAPI, Request
import logging, time

import uuid
app = FastAPI()
# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.middleware("http")
async def request_id_logging(request: Request, call_next):
    # Generate a UUID for traceability
    request_id = str(uuid.uuid4())

    # Record start time
    start_time = time.time()
    response = await call_next(request)
    #random_letters = "".join(random.choice(string.ascii_letters) for _ in range(10))
    # Calculate latency
    process_time = time.time() - start_time

    # Attach request ID to response headers
    response.headers["X-Request-ID"] = request_id

    # Log structured info
    logging.info(
        f"Request {request.method} {request.url.path} "
        f"completed in {process_time:.4f}s "
        f"with Request-ID={request_id}"
    )
    return response



@app.get("/")
async def say_hi():
    return {"message": "Hi, I am hi"}