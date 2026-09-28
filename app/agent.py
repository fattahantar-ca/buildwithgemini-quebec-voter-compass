# ruff: noqa
import json
import re
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.cloud import firestore
from google.genai import types

PROJECT_ID = "qwiklabs-gcp-01-21daa4813152"
db = firestore.Client(project=PROJECT_ID)


def compare_issue_platforms(issue_category: str) -> str:
    """Compares the platforms and key promises of all major Quebec political parties for a specific issue category.

    Args:
        issue_category: The policy topic to compare (e.g. "Cost of Living", "Health Care", "Education", "Child Care", "Economy & Tariffs", "Environment & Natural Resources").

    Returns:
        JSON string containing the side-by-side promises of CAQ, PLQ, QS, PQ, and PCQ for the issue.
    """
    col_ref = db.collection("quebec_2026_platforms")
    docs = list(col_ref.stream())

    category_lower = issue_category.lower().strip()
    target_slug = category_lower.replace(" ", "-")

    matched_doc = None

    # First attempt: exact match on document ID or slug
    for doc in docs:
        if doc.id == target_slug or target_slug in doc.id:
            matched_doc = doc.to_dict()
            break

    # Second attempt: check if major keywords match (e.g. "health" -> "health-care")
    if not matched_doc:
        for doc in docs:
            data = doc.to_dict()
            issue_id = doc.id
            if any(w in category_lower for w in ["health", "hospital", "doctor", "ramq", "medicare"]) and "health" in issue_id:
                matched_doc = data
                break
            elif any(w in category_lower for w in ["child", "daycare", "cpe", "family"]) and "child" in issue_id:
                matched_doc = data
                break
            elif any(w in category_lower for w in ["cost", "tax", "living", "exemption", "income", "inflation"]) and "cost" in issue_id:
                matched_doc = data
                break
            elif any(w in category_lower for w in ["economy", "tariff", "job", "business", "sme"]) and "economy" in issue_id:
                matched_doc = data
                break
            elif any(w in category_lower for w in ["education", "school", "french", "language", "teacher"]) and "education" in issue_id:
                matched_doc = data
                break
            elif any(w in category_lower for w in ["environment", "energy", "carbon", "nature", "climate", "green"]) and "environment" in issue_id:
                matched_doc = data
                break

    if not matched_doc:
        return json.dumps({
            "error": f"Issue category '{issue_category}' not found.",
            "available_issues": [d.to_dict().get("issue_name") for d in docs]
        }, indent=2)

    return json.dumps({
        "issue_id": matched_doc.get("issue_id"),
        "issue_name": matched_doc.get("issue_name"),
        "parties": matched_doc.get("parties", {})
    }, indent=2)


def get_party_platform(party_name: str) -> str:
    """Retrieves all policy platform promises for a specific Quebec political party across all issues.

    Args:
        party_name: Name or acronym of the party (e.g. "CAQ", "Liberal", "PLQ", "Québec Solidaire", "QS", "Parti Québécois", "PQ", "Conservative", "PCQ").

    Returns:
        JSON string containing the party's platform promises across all issue categories.
    """
    p_lower = party_name.lower().strip()

    key_map = {
        "caq": "caq", "coalition avenir québec": "caq", "coalition avenir quebec": "caq",
        "plq": "plq", "quebec liberal party": "plq", "liberal": "plq", "parti libéral": "plq",
        "qs": "qs", "québec solidaire": "qs", "quebec solidaire": "qs", "solidaire": "qs",
        "pq": "pq", "parti québécois": "pq", "parti quebecois": "pq", "pequiste": "pq",
        "pcq": "pcq", "conservative party of quebec": "pcq", "conservative": "pcq"
    }

    target_key = key_map.get(p_lower)
    if not target_key:
        for k, v in key_map.items():
            if k in p_lower or p_lower in k:
                target_key = v
                break

    if not target_key:
        return json.dumps({
            "error": f"Party '{party_name}' not recognized. Supported parties: CAQ, PLQ, QS, PQ, PCQ."
        })

    col_ref = db.collection("quebec_2026_platforms")
    docs = col_ref.stream()

    platform_summary = []
    party_details = None

    for doc in docs:
        data = doc.to_dict()
        issue_name = data.get("issue_name")
        parties = data.get("parties", {})
        party_info = parties.get(target_key)

        if party_info:
            if not party_details:
                party_details = {
                    "party_name": party_info.get("party_name"),
                    "leader": party_info.get("leader"),
                    "color": party_info.get("color")
                }
            platform_summary.append({
                "issue": issue_name,
                "promises": party_info.get("key_promises", [])
            })

    return json.dumps({
        "party_info": party_details,
        "platform_promises": platform_summary
    }, indent=2)


def find_matching_parties(user_priorities: list[str]) -> str:
    """Evaluates a voter's priorities against the platforms of all 5 major parties to highlight alignment.

    Args:
        user_priorities: List of key issues or policy goals important to the voter.

    Returns:
        JSON string listing matched promises per party for the voter's stated priorities.
    """
    col_ref = db.collection("quebec_2026_platforms")
    docs = list(col_ref.stream())

    matches_by_party = {
        "caq": {"party_name": "Coalition Avenir Québec", "matches": []},
        "plq": {"party_name": "Quebec Liberal Party", "matches": []},
        "qs": {"party_name": "Québec Solidaire", "matches": []},
        "pq": {"party_name": "Parti Québécois", "matches": []},
        "pcq": {"party_name": "Conservative Party of Quebec", "matches": []},
    }

    for doc in docs:
        data = doc.to_dict()
        issue_name = data.get("issue_name")
        parties = data.get("parties", {})

        for priority in user_priorities:
            p_lower = priority.lower().strip()
            for party_key, party_info in parties.items():
                if party_key in matches_by_party:
                    promises = party_info.get("key_promises", [])
                    matching_promises = [prom for prom in promises if any(term in prom.lower() for term in p_lower.split())]
                    if matching_promises:
                        matches_by_party[party_key]["matches"].append({
                            "priority_topic": priority,
                            "issue_category": issue_name,
                            "promises": matching_promises
                        })

    return json.dumps({
        "voter_priorities": user_priorities,
        "party_alignment_analysis": matches_by_party
    }, indent=2)


from pathlib import Path
from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager

try:
    from .a2ui_utils import a2ui_callback
except ImportError:
    from app.a2ui_utils import a2ui_callback

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are Quebec Voter Compass 2026, an objective, non-partisan AI provincial election assistant. "
        "Your mission is to help voters understand and compare the platform commitments, policy positions, "
        "and election promises of Quebec's 5 major political parties (Coalition Avenir Québec, Quebec Liberal Party, "
        "Québec Solidaire, Parti Québécois, Conservative Party of Quebec) for the 2026 provincial election. "
        "Always call your policy comparison tools to retrieve official party data from Firestore, and present neutral, factual comparisons."
    ),
    workflow_description="Analyze voter queries, call comparison tools, and output structured A2UI surface cards when presenting party platform comparisons.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="quebec_voter_compass_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    tools=[
        compare_issue_platforms,
        get_party_platform,
        find_matching_parties,
    ],
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
