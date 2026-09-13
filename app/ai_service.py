from __future__ import annotations

import re
from dataclasses import dataclass

from app.models import AIExtraction, LeadInput
from app.rules import normalize_service


@dataclass
class HeuristicAIService:
    """
    Offline, deterministic extractor used by default.

    It makes the repository runnable without external credentials.
    Replace this implementation with your preferred AI provider in production.
    """

    service_keywords: dict[str, tuple[str, ...]] = None

    def __post_init__(self) -> None:
        if self.service_keywords is None:
            self.service_keywords = {
                "crm_automation": (
                    "crm",
                    "lead routing",
                    "sales automation",
                    "follow-up automation",
                    "follow up automation",
                    "whatsapp automation",
                ),
                "ai_automation": (
                    "ai automation",
                    "ai agent",
                    "chatbot",
                    "artificial intelligence",
                ),
                "seo": (
                    "seo",
                    "search engine optimization",
                    "organic traffic",
                    "technical seo",
                ),
                "paid_media": (
                    "google ads",
                    "meta ads",
                    "paid media",
                    "ppc",
                    "facebook ads",
                ),
            }

    def extract(self, lead: LeadInput) -> AIExtraction:
        text = " ".join(
            value
            for value in [
                lead.service_interest,
                lead.message,
                lead.company,
                lead.location,
                lead.timeline,
            ]
            if value
        ).lower()

        service = normalize_service(lead.service_interest)

        if not service:
            matches: list[str] = []
            for candidate, keywords in self.service_keywords.items():
                if any(keyword in text for keyword in keywords):
                    matches.append(candidate)
            if len(matches) == 1:
                service = matches[0]
            elif len(matches) > 1:
                service = matches[0]

        budget = lead.budget
        if budget is None:
            budget_match = re.search(
                r"(?:budget|spend|investment)[^0-9]{0,12}(?:₹|rs\.?|inr)?\s*([0-9][0-9,]*)",
                text,
                flags=re.IGNORECASE,
            )
            if budget_match:
                budget = float(budget_match.group(1).replace(",", ""))

        timeline = lead.timeline
        if timeline is None:
            timeline_match = re.search(
                r"\b(?:within\s+)?(\d+\s*(?:day|days|week|weeks|month|months))\b",
                text,
                flags=re.IGNORECASE,
            )
            if timeline_match:
                timeline = timeline_match.group(1)

        meaningful_words = [
            word
            for word in re.findall(r"[a-zA-Z0-9]+", lead.message)
            if len(word) > 2
        ]
        requirement_summary = lead.message.strip()
        if len(requirement_summary) > 240:
            requirement_summary = requirement_summary[:237].rstrip() + "..."

        needs_clarification = len(meaningful_words) < 4
        human_reason = None
        if not service:
            human_reason = "Service interest could not be identified."
            needs_clarification = True

        commercial_terms = (
            "discount",
            "custom pricing",
            "negotiate",
            "contract",
            "legal terms",
        )
        if any(term in text for term in commercial_terms):
            human_reason = "Commercial or contractual discussion requires human review."

        return AIExtraction(
            service_interest=service,
            requirement_summary=requirement_summary,
            location=lead.location,
            timeline=timeline,
            budget=budget,
            needs_clarification=needs_clarification,
            human_review_reason=human_reason,
        )
