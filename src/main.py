import sentry_sdk
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.auth.schemas import UserRead, UserUpdate
from src.auth.users import current_active_user, fastapi_users
from src.config import app_configs, settings
from src.database import User
from src.eat_list.router import router as eat_list_router
from src.product.router import router as product_router
from src.user_product.router import router as user_product_router

app = FastAPI(**app_configs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {
        "message": f"Hello {user.username if user.username else user.email}! Your id is: '{user.id}'"
    }


app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(product_router, prefix="/products", tags=["product"])
app.include_router(eat_list_router, prefix="/eat_lists", tags=["eat_lists"])
app.include_router(user_product_router, prefix="/user_products", tags=["user_products"])
