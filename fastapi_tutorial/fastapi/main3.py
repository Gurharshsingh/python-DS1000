from fastapi import FastAPI
from api.data import router as data_router
from api.filehandle import router as file_router
from api.auth_router import router as auth_router
from api.user_router import router as user_router
from database.database import create_table
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="JWT Authentication Part-1")

create_table()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(data_router)
app.include_router(file_router)



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title="FastAPI",
        version="0.1.0",
        routes=app.routes,
    )
    for component in openapi_schema.get("components", {}).get("schemas", {}).values():
        properties = component.get("properties", {})
        for prop in properties.values():
            if prop.get("contentMediaType") == "application/octet-stream":
                prop["format"] = "binary"
            elif prop.get("type") == "array" and isinstance(prop.get("items"), dict):
                items = prop["items"]
                if items.get("contentMediaType") == "application/octet-stream":
                    items["format"] = "binary"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi