from typing import TypedDict


class SchemaMetadata(TypedDict):
    id: str
    name: str
    description: str
    category: str
    icon: str
    system_prompt: str
    example_text: str


SCHEMA_METADATA: dict[str, SchemaMetadata] = {
    "contact": {
        "id": "contact",
        "name": "Contact Information",
        "description": "Extract contact details like name, email, phone, and company",
        "category": "basic",
        "icon": "user",
        "system_prompt": """Extract contact information in this EXACT JSON structure:

{
  "name": "Full name of person",
  "email": "email@example.com or null",
  "phone": "+1-555-0123 or null",
  "company": "Company name or null"
}

RULES:
- name is REQUIRED (string)
- email, phone, company are OPTIONAL (string or null)
- Only extract explicitly mentioned information
- Use null for missing fields, not empty strings""",
        "example_text": "Contact Sarah Johnson at sarah.johnson@techcorp.com or call +1-555-0123. She works at TechCorp.",
    },
    "job_posting": {
        "id": "job_posting",
        "name": "Job Posting Parser",
        "description": "Extract job title, company, location, salary, and requirements",
        "category": "basic",
        "icon": "briefcase",
        "system_prompt": """Extract job posting information in this EXACT JSON structure:

{
  "title": "Senior Software Engineer",
  "company": "TechCorp Inc",
  "location": "San Francisco, CA or null",
  "salary_range": "$120k-$180k or null",
  "job_type": "Full-time or null",
  "experience_level": "Senior or null",
  "description": "We are looking for a talented engineer...",
  "requirements": "5+ years Python experience, BS in CS or null",
  "posted_date": "March 15, 2024 or null"
}

CRITICAL RULES:
- title is REQUIRED (string)
- company is REQUIRED (string)
- description is REQUIRED (string)
- All other fields are OPTIONAL (string or null)
- job_type examples: Full-time, Part-time, Contract, Internship
- experience_level examples: Entry, Mid, Senior, Lead, Executive
- Extract salary range as a single string (e.g., "$80k-$120k", "Competitive")
- If requirements are listed, combine them into a single descriptive string""",
        "example_text": "Senior Software Engineer at TechCorp Inc, San Francisco. $120k-$180k, Full-time. We're seeking an experienced engineer to build scalable systems. Requirements: 5+ years Python, BS in Computer Science. Posted March 15, 2024.",
    },
    "event": {
        "id": "event",
        "name": "Event Details",
        "description": "Extract event name, date, location, and attendees",
        "category": "basic",
        "icon": "calendar",
        "system_prompt": """Extract event information in this EXACT JSON structure:

{
  "name": "Event Name",
  "date": "March 15, 2025",
  "location": "San Francisco Convention Center or null",
  "attendees": ["Sarah", "Mike", "Emily"]
}

CRITICAL RULES:
- name is REQUIRED (string)
- date is REQUIRED (string, any format)
- location is OPTIONAL (string or null)
- attendees MUST be an ARRAY of STRINGS (can be empty array [])
- Extract all mentioned attendee names
- If no attendees mentioned, use empty array []""",
        "example_text": "Join us for the Tech Conference on March 15, 2025 at San Francisco Convention Center. Attendees: Sarah, Mike, Emily.",
    },
    "bug_report": {
        "id": "bug_report",
        "name": "GitHub Issue Parser",
        "description": "Extract bug reports with severity, steps to reproduce, and environment details",
        "category": "advanced",
        "icon": "bug",
        "system_prompt": """You are an expert at analyzing bug reports and GitHub issues.

Extract the following information in the exact JSON structure:

{
  "title": "Brief summary",
  "description": "Detailed explanation",
  "steps_to_reproduce": ["Step 1", "Step 2", "Step 3"],
  "expected_behavior": "What should happen",
  "actual_behavior": "What actually happens",
  "severity": "critical",
  "environment": "OS, browser, version details or null",
  "affected_version": "Version number or null",
  "labels": ["bug", "ui", "critical"],
  "error_logs": "Stack traces or null"
}

CRITICAL RULES:
1. severity MUST be EXACTLY one of: "low", "medium", "high", "critical" (lowercase only)
2. steps_to_reproduce MUST be an array of strings, even if only one step
3. labels MUST be an array of strings
4. Use null for missing optional fields (environment, affected_version, error_logs)

SEVERITY CLASSIFICATION:
- "critical": Crashes, data loss, blocks all users, blocking releases
- "high": Major features broken, affects many users
- "medium": Inconvenient but has workarounds
- "low": Minor cosmetic issues

If information is not explicitly mentioned, use reasonable defaults or null.""",
        "example_text": "App crashes when clicking submit. Steps: 1. Fill form 2. Click submit. Expected: Form submits. Actual: App crashes with NullPointerException. Version 2.3.1, Chrome 120, Ubuntu. Blocking release!",
    },
}


def get_schema_metadata(schema_id: str) -> SchemaMetadata | None:
    return SCHEMA_METADATA.get(schema_id)


def list_all_schemas() -> list[SchemaMetadata]:
    return list(SCHEMA_METADATA.values())


def get_schemas_by_category(category: str) -> list[SchemaMetadata]:
    return [
        schema
        for schema in SCHEMA_METADATA.values()
        if schema["category"] == category
    ]
