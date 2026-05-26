from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

resource = Resource.create({"service.name": "posts-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector.app-cicd:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    content: str

posts_db = []

@app.post("/posts")
async def create_post(post: Post):
    with tracer.start_as_current_span("create_post"):
        posts_db.append(post)
        return {"status": "success", "post": post}

@app.get("/posts")
async def list_posts():
    with tracer.start_as_current_span("list_posts"):
        return posts_db

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "posts-service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
