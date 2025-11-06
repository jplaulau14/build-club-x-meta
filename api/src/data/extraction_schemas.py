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
        "system_prompt": """You are a contact information extraction expert.

Extract the following information from the text:
- Name: Full name of the person
- Email: Email address
- Phone: Phone number (any format)
- Company: Organization or company name

Only extract information that is explicitly mentioned. If a field is not present, leave it as null.
Be precise and accurate.""",
        "example_text": "Contact Sarah Johnson at sarah.johnson@techcorp.com or call +1-555-0123. She works at TechCorp.",
    },
    "recipe": {
        "id": "recipe",
        "name": "Recipe Parser",
        "description": "Extract recipe title, ingredients, instructions, and prep time",
        "category": "basic",
        "icon": "utensils",
        "system_prompt": """You are a recipe extraction expert.

Extract the following from recipe text:
- Title: Name of the dish
- Ingredients: List with name, quantity, and unit for each ingredient
- Instructions: Step-by-step cooking instructions as a list
- Prep time: Total preparation and cooking time

Be thorough with ingredients - capture quantity and units. Break down instructions into clear steps.""",
        "example_text": "Chocolate Chip Cookies: Mix 2 cups flour, 1 cup butter, 1 cup sugar. Add eggs. Bake at 350F for 12 minutes. Prep: 20 min.",
    },
    "event": {
        "id": "event",
        "name": "Event Details",
        "description": "Extract event name, date, location, and attendees",
        "category": "basic",
        "icon": "calendar",
        "system_prompt": """You are an event information extraction expert.

Extract the following from event descriptions:
- Name: Event title or name
- Date: When the event occurs (any date format)
- Location: Where the event takes place
- Attendees: List of people attending or invited

Parse dates in natural language. Extract all mentioned attendees.""",
        "example_text": "Join us for the Tech Conference on March 15, 2025 at San Francisco Convention Center. Attendees: Sarah, Mike, Emily.",
    },
    "bug_report": {
        "id": "bug_report",
        "name": "GitHub Issue Parser",
        "description": "Extract bug reports with severity, steps to reproduce, and environment details",
        "category": "advanced",
        "icon": "bug",
        "system_prompt": """You are an expert at analyzing bug reports and GitHub issues.

Extract the following information:
- Title: Brief summary of the issue
- Description: Detailed explanation of the problem
- Steps to reproduce: Clear numbered steps to recreate the bug
- Expected behavior: What should happen
- Actual behavior: What actually happens
- Severity: Classify as "low", "medium", "high", or "critical" based on impact
- Environment: OS, browser, version details (if mentioned)
- Affected version: Software/app version where bug occurs
- Labels: Categorize with relevant tags (e.g., "bug", "ui", "performance", "regression")
- Error logs: Stack traces or error messages (if present)

SEVERITY GUIDELINES:
- Critical: Crashes, data loss, security issues, complete feature breakdown
- High: Major functionality broken, blocking user workflows
- Medium: Significant inconvenience but workarounds exist
- Low: Minor issues, cosmetic problems, edge cases

LABELS: Suggest appropriate labels based on content (e.g., "ui" for interface issues, "api" for backend, "performance" for speed issues).

Only extract what's explicitly mentioned. Infer severity intelligently from the description.""",
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
