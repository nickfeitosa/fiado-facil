from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import crud, schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fiado Fácil",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get(
    "/api/clients",
    response_model=list[schemas.ClientListItem]
)
def get_clients(
    db: Session = Depends(get_db)
):
    return crud.list_clients(db)


@app.post(
    "/api/clients",
    response_model=schemas.ClientOut,
    status_code=201
)
def post_client(
    payload: schemas.ClientCreate,
    db: Session = Depends(get_db)
):
    return crud.create_client(db, payload)


@app.get(
    "/api/purchases",
    response_model=list[schemas.PurchaseOut]
)
def get_purchases(
    db: Session = Depends(get_db)
):
    return crud.list_purchases(db)


@app.post(
    "/api/purchases",
    response_model=schemas.PurchaseCreateResponse,
    status_code=201
)
def post_purchase(
    payload: schemas.PurchaseCreate,
    db: Session = Depends(get_db)
):
    created = crud.create_purchase(
        db,
        payload
    )

    if not created:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return created


@app.get(
    "/api/dashboard",
    response_model=schemas.DashboardOut
)
def dashboard(
    db: Session = Depends(get_db)
):
    return crud.get_dashboard(db)


app.mount(
    "/static",
    StaticFiles(directory=PUBLIC_DIR),
    name="static"
)


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    return FileResponse(
        PUBLIC_DIR / "index.html"
    )