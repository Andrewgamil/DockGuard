import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlmodel import Session, SQLModel, create_engine, select

from config import settings
from models import Link

# Database Setup
engine = create_engine(settings.DATABASE_URL, echo=False)

# Prometheus Metrics
urls_shortened_counter = Counter(
    "urls_shortened_total", "Total number of URLs successfully shortened"
)

successful_redirects_counter = Counter(
    "successful_redirects_total", "Total number of successful redirects"
)

failed_lookups_counter = Counter(
    "failed_lookups_total", "Total number of failed lookups (404 errors)"
)

request_latency_histogram = Histogram(
    "request_latency_seconds", "Request latency in seconds", ["endpoint", "method"]
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# App Setup
app = FastAPI(title="LinkShrink", version="2.0")
templates = Jinja2Templates(directory="frontend")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/hafbujibhadnsufiadhsbniufj")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


def create_slug(length: int = 5) -> str:
    return secrets.token_urlsafe(length)[:length]


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/generate")
def generate_link(payload: dict, db: Session = Depends(get_session)):
    start_time = time.time()

    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=422, detail="URL is required")

    slug = create_slug()

    # Create the link object
    new_link = Link(slug=slug, target_url=url)

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    # Increment counter for successful URL shortening
    urls_shortened_counter.inc()

    # Track request latency
    request_latency_histogram.labels(endpoint="/api/generate", method="POST").observe(
        time.time() - start_time
    )

    # Return specific fields to avoid Pydantic recursion errors
    return {"slug": new_link.slug, "original": new_link.target_url}


@app.get("/{slug}")
def redirect_link(slug: str, db: Session = Depends(get_session)):
    start_time = time.time()

    statement = select(Link).where(Link.slug == slug)
    result = db.exec(statement).first()

    if not result:
        # Increment counter for failed lookups
        failed_lookups_counter.inc()
        request_latency_histogram.labels(endpoint="/{slug}", method="GET").observe(
            time.time() - start_time
        )
        return HTMLResponse(content="<h1>404 - Link Not Found</h1>", status_code=404)

    result.clicks += 1
    db.add(result)
    db.commit()

    # Increment counter for successful redirects
    successful_redirects_counter.inc()

    # Track request latency
    request_latency_histogram.labels(endpoint="/{slug}", method="GET").observe(
        time.time() - start_time
    )

    return RedirectResponse(result.target_url)
