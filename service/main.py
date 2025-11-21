import secrets
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlmodel import Session, SQLModel, create_engine, select

from models import Link


DATABASE_URL = "sqlite:///./data/urlshort.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


urlshort_created_total = Counter(
    "urlshort_created_total", "Total number of URLs successfully shortened"
)

urlshort_redirects_total = Counter(
    "urlshort_redirects_total", "Total number of successful redirects"
)

urlshort_404_total = Counter(
    "urlshort_404_total", "Total number of failed lookups (404 errors)"
)

urlshort_request_latency_seconds = Histogram(
    "urlshort_request_latency_seconds",
    "Request latency in seconds",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)


def init_db():
    
    SQLModel.metadata.create_all(engine)


def get_session():
   
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    init_db()
    yield


# App Setup
app = FastAPI(title="URL Shortener", version="1.0", lifespan=lifespan)


@app.get("/metrics")
async def metrics():
   
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


def create_short_code(length: int = 6) -> str:
    
    return secrets.token_urlsafe(length)[:length].replace("-", "").replace("_", "")[:length]


@app.post("/shorten")
async def shorten_url(payload: dict, db: Session = Depends(get_session)):
   
    start_time = time.time()
    
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    

    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
  
    short_code = create_short_code()
    
    
    while True:
        existing = db.exec(select(Link).where(Link.short_code == short_code)).first()
        if not existing:
            break
        short_code = create_short_code()
    
   
    new_link = Link(short_code=short_code, original_url=url)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    
 
    urlshort_created_total.inc()
    
   
    urlshort_request_latency_seconds.observe(time.time() - start_time)
    
    return {"short_code": new_link.short_code}


@app.get("/{short_code}")
async def redirect_to_url(short_code: str, db: Session = Depends(get_session)):
   
    start_time = time.time()
    
   
    link = db.exec(select(Link).where(Link.short_code == short_code)).first()
    
    if not link:
       
        urlshort_404_total.inc()
        urlshort_request_latency_seconds.observe(time.time() - start_time)
        raise HTTPException(status_code=404, detail="Short code not found")
    
   
    link.clicks += 1
    db.add(link)
    db.commit()
    
  
    urlshort_redirects_total.inc()
    
    
    urlshort_request_latency_seconds.observe(time.time() - start_time)
    
    return RedirectResponse(url=link.original_url, status_code=302)


