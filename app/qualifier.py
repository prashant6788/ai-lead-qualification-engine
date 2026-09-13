from __future__ import annotations

from app.ai_service import HeuristicAIService
from app.models import (
    LeadInput,
    QualificationBreakdown,
    QualificationResult,
)
from app.rules import is_supported_service, load_rules, normalize_service


class LeadQualifier:
    def __init__(self, rules: dict | None = None, ai_service=None) -> None:
        self.rules = rules or load_rules()
        self.ai_service = ai_service or HeuristicAIService()

    def qualify(self, lead: LeadInput) -> QualificationResult:
        extracted = self.ai_service.extract(lead)
        scoring = self.rules["scoring"]
        thresholds = self.rules["thresholds"]

        service = normalize_service(extracted.service_interest)
        supported = is_supported_service(service, self.rules)

        breakdown = QualificationBreakdown(
            supported_service=scoring["supported_service"] if supported else 0,
            clear_requirement=scoring["clear_requirement"]
            if extracted.requirement_summary and not extracted.needs_clarification
            else 0,
            budget_available=scoring["budget_available"]
            if extracted.budget is not None
            else 0,
            timeline_available=scoring["timeline_available"]
            if extracted.timeline
            else 0,
            target_location=scoring["target_location"]
            if extracted.location
            else 0,
            business_identified=scoring["business_identified"]
            if lead.company
            else 0,
        )

        score = sum(breakdown.model_dump().values())
        review_reason = extracted.human_review_reason

        force_human_review = bool(review_reason)
        if extracted.needs_clarification and not review_reason:
            review_reason = "The lead does not contain enough information for a reliable automated decision."
            force_human_review = True

        if not supported:
            review_reason = review_reason or "Service is unsupported or unclear."
            force_human_review = True

        if force_human_review:
            status = "review"
            action = (
                "request_clarification"
                if extracted.needs_clarification and not extracted.human_review_reason
                else "human_review"
            )
        elif score >= thresholds["qualified"]:
            status = "qualified"
            action = "book_sales_call"
        elif score >= thresholds["human_review"]:
            status = "review"
            action = "human_review"
            review_reason = review_reason or "Lead falls within the configurable human-review score range."
        else:
            status = "not_qualified"
            action = "nurture"

        return QualificationResult(
            qualification_status=status,
            score=score,
            service_interest=service,
            requirement_summary=extracted.requirement_summary,
            needs_human_review=status == "review",
            review_reason=review_reason if status == "review" else None,
            recommended_action=action,
            breakdown=breakdown,
        )
