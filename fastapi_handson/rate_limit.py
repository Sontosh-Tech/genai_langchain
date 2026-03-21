from fastapi import FastAPI, Request, Response
import logging, time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from collections import defaultdict
from typing import Dict
import uuid

app = FastAPI()

class RateLimitClass(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log(self, msg: str):
        print(msg)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if path.startswith("/docs") or path.startswith("/openapi.json") or path.startswith("/redoc"):
            return await call_next(request)

        client_ip = request.client.host
        current_time = time.time()
        if current_time - self.rate_limit_records[client_ip] < 1:
            return Response(content=f"Rate limit Exceeded", status_code=429)

        self.rate_limit_records[client_ip] = current_time

        await self.log(f"Request to {path}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        #custom_header = {"X_Process_Time": str(process_time)}
        response.headers["X_Process_Time"] = str(process_time)
        #for header, value in custom_header.items():
        #    response.headers.append(header, value)

        await self.log(f"Response for {path} took {process_time} seconds")

        return  response

app.add_middleware(RateLimitClass)


@app.get("/check")
async def say_hi():
    return {"message": "Hi, I am rate limit demo"}