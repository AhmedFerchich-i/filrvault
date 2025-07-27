from fastapi import FastAPI
from api import upload
from api import manage
from api import health
from core.db import Base, engine
from api import user
from api import auth
app = FastAPI(title="File Vault")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(manage.router, prefix="/manage", tags=["Manage"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(user.router,prefix="/users",tags=["Users"])
app.include_router(auth.router,prefix='/auth',tags=['Authentication'])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)