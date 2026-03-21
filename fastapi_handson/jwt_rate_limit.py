from fastapi import FastAPI, Request, Response, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
#import aioredis
import time
import logging
import uuid
import jwt
import redis.asyncio as redis

# -------------------------
# App setup
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

'''
@app.on_event("startup")
async def startup_event():
    app.state.redis = await redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()
'''
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis = await redis.from_url("redis://localhost", decode_responses=True)
    yield
    # Shutdown
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)

# -------------------------
# JWT setup
# -------------------------
JWT_SECRET = "supersecretkey"   # store securely in production!
JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE = 60 * 15   # 15 minutes
REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 7  # 7 days
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(username: str, tier: str):
    payload = {
        "sub": username,
        "tier": tier,
        "iat": int(time.time()),
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(username: str):
    payload = {
        "sub": username,
        "type": "refresh",
        "iat": int(time.time()),
        "exp": int(time.time()) + REFRESH_TOKEN_EXPIRE
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# Fake user DB
# -------------------------
fake_users_db = {
    "alice": {"password": "alice123", "tier": "free"},
    "bob": {"password": "bob123", "tier": "premium"},
    "carol": {"password": "carol123", "tier": "enterprise"},
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    return payload

# -------------------------
# Rate limits per tier
# -------------------------
TIER_LIMITS = {
    "free": 1,
    "premium": 5,
    "enterprise": 20
}

# -------------------------
# Middleware
# -------------------------
class JWTTierRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host
        path = request.url.path
        request_id = str(uuid.uuid4())

        # Skip login/refresh endpoints
        if path in ["/login", "/refresh"]:
            return await call_next(request)

        # Extract JWT
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(content="Missing or invalid Authorization header", status_code=401)

        token = auth_header.split(" ")[1]
        payload = decode_jwt(token)

        if payload.get("tier") is None:
            return Response(content="Invalid access token", status_code=401)

        api_tier = payload.get("tier", "free").lower()
        limit_per_second = TIER_LIMITS.get(api_tier, TIER_LIMITS["free"])

        # Redis key per client + tier
        key = f"rate_limit:{client_ip}:{api_tier}"

        last_request_time = await redis.get(key)
        current_time = time.time()

        if last_request_time and current_time - float(last_request_time) < 1 / limit_per_second:
            logging.warning(f"Rate limit exceeded for {client_ip} ({api_tier}) on {path}")
            return Response(content="Rate limit exceeded", status_code=429)

        await redis.set(key, current_time, ex=1)

        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-API-Tier"] = api_tier

        logging.info(
            f"Request {request.method} {path} from {client_ip} "
            f"(tier={api_tier}) completed in {process_time:.4f}s "
            f"with Request-ID={request_id}"
        )

        return response

app.add_middleware(JWTTierRateLimitMiddleware)

# -------------------------
# Endpoints
# -------------------------
@app.post("/login1")
async def login1(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(form_data.username, user["tier"])
    refresh_token = create_refresh_token(form_data.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(form_data.username)
    refresh_token = create_refresh_token(form_data.username)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_jwt(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload["sub"]
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(username, user["tier"])
    return {"access_token": new_access_token, "token_type": "bearer"}

@app.get("/demo")
async def demo_endpoint():
    return {"message": "This is a JWT tiered rate limit demo with refresh tokens"}


@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['sub']}, you are authorized!"}

