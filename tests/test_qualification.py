from app.models import LeadInput
from app.qualifier import LeadQualifier


def test_qualified_lead():
    qualifier = LeadQualifier()
    lead = LeadInput(
        name="Rahul Sharma",
        company="Northstar Realty",
        message="We need CRM automation and WhatsApp follow-up for our inbound leads.",
        service_interest="crm_automation",
        location="Gurugram",
        budget=50000,
        timeline="30 days",
    )

    result = qualifier.qualify(lead)

    assert result.qualification_status == "qualified"
    assert result.score == 100
    assert result.needs_human_review is False
    assert result.recommended_action == "book_sales_call"


def test_ambiguous_lead_goes_to_review():
    qualifier = LeadQualifier()
    lead = LeadInput(
        name="Demo User",
        message="Please contact me.",
    )

    result = qualifier.qualify(lead)

    assert result.qualification_status == "review"
    assert result.needs_human_review is True
    assert result.recommended_action in {"human_review", "request_clarification"}


def test_commercial_negotiation_requires_human_review():
    qualifier = LeadQualifier()
    lead = LeadInput(
        name="Anita Mehta",
        company="Example Consulting",
        message="We need CRM automation. Can you offer a discount for a long contract?",
        service_interest="crm_automation",
        location="Delhi",
        budget=60000,
        timeline="1 month",
    )

    result = qualifier.qualify(lead)

    assert result.qualification_status == "review"
    assert result.needs_human_review is True
    assert "Commercial" in (result.review_reason or "")


def test_lower_score_can_be_not_qualified_when_service_is_supported():
    qualifier = LeadQualifier()
    lead = LeadInput(
        name="Example",
        message="Need SEO.",
        service_interest="seo",
    )

    result = qualifier.qualify(lead)

    assert result.score < 50
    assert result.qualification_status in {"review", "not_qualified"}
