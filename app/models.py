from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


QualificationStatus = Literal["qualified", "review", "not_qualified"]
RecommendedAction = Literal[
    "book_sales_call",
    "human_review",
    "nurture",
    "request_clarification",
]


class LeadInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    company: Optional[str] = Field(default=None, max_length=160)
    email: Optional[str] = Field(default=None, max_length=254)
    phone: Optional[str] = Field(default=None, max_length=40)
    message: str = Field(min_length=1, max_length=5000)
    service_interest: Optional[str] = Field(default=None, max_length=120)
    location: Optional[str] = Field(default=None, max_length=120)
    budget: Optional[float] = Field(default=None, ge=0)
    timeline: Optional[str] = Field(default=None, max_length=120)
    lead_source: Optional[str] = Field(default=None, max_length=120)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return value.strip().lower() or None

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = "".join(ch for ch in value if ch.isdigit() or ch == "+")
        return cleaned or None


class AIExtraction(BaseModel):
    service_interest: Optional[str] = None
    requirement_summary: str = ""
    location: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[float] = None
    needs_clarification: bool = False
    human_review_reason: Optional[str] = None


class QualificationBreakdown(BaseModel):
    supported_service: int = 0
    clear_requirement: int = 0
    budget_available: int = 0
    timeline_available: int = 0
    target_location: int = 0
    business_identified: int = 0


class QualificationResult(BaseModel):
    qualification_status: QualificationStatus
    score: int = Field(ge=0, le=100)
    service_interest: Optional[str]
    requirement_summary: str
    needs_human_review: bool
    review_reason: Optional[str] = None
    recommended_action: RecommendedAction
    breakdown: QualificationBreakdown
