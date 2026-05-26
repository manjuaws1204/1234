from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# OpenTelemetry setup
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configure tracer for comments-service
resource = Resource.create({"service.name": "comments-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector.app-cicd:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

app = FastAPI()

class Comment(BaseModel):
    id: int
    post_id: int
    text: str

comments_db = []

@app.post("/comments")
async def add_comment(comment: Comment):
    with tracer.start_as_current_span("add_comment"):
        comments_db.append(comment)
        return {"status": "success", "comment": comment}

@app.get("/comments/{post_id}")
async def get_comments(post_id: int):
    with tracer.start_as_current_span("get_comments"):
        filtered = [c for c in comments_db if c.post_id == post_id]
        return {"post_id": post_id, "comments": filtered}

@app.post("/init")
async def init_post(post_id: int):
    with tracer.start_as_current_span("init_post"):
        # Placeholder for initializing comments for a new post
        return {"status": "initialized", "post_id": post_id}

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "comments-service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
