from fastapi import FastAPI

from app.models import LeadInput, QualificationResult
from app.qualifier import LeadQualifier

app = FastAPI(
    title="AI Lead Qualification Engine",
    description=(
        "Reference implementation for AI-assisted lead qualification using "
        "structured extraction, deterministic scoring and human-review fallback."
    ),
    version="1.0.0",
)

qualifier = LeadQualifier()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/qualify", response_model=QualificationResult)
def qualify_lead(lead: LeadInput) -> QualificationResult:
    return qualifier.qualify(lead)
