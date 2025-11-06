CONTACT_EXAMPLES = [
    {
        "name": "Complete Contact",
        "text": "For more information, contact Sarah Johnson at sarah.johnson@techcorp.com or call her at +1-555-0123. She works at TechCorp as the Head of Engineering.",
    },
    {
        "name": "Minimal Contact (name and email only)",
        "text": "Please reach out to Michael Chen at michael.chen@startup.io for any questions.",
    },
    {
        "name": "Email Signature",
        "text": """Best regards,
        Dr. Emily Rodriguez
        Chief Technology Officer
        InnovateLabs Inc.
        emily.rodriguez@innovatelabs.com
        Office: +1-555-0199
        Mobile: +1-555-0198""",
    },
]

RECIPE_EXAMPLES = [
    {
        "name": "Detailed Recipe",
        "text": """Classic Chocolate Chip Cookies

        Ingredients:
        - 2 cups all-purpose flour
        - 1 cup butter, softened
        - 3/4 cup granulated sugar
        - 2 large eggs
        - 1 cup chocolate chips
        - 1 teaspoon vanilla extract

        Instructions:
        1. Preheat your oven to 350°F (175°C)
        2. In a large bowl, cream together butter and sugar until fluffy
        3. Beat in eggs and vanilla extract
        4. Gradually blend in flour
        5. Stir in chocolate chips
        6. Drop rounded tablespoons of dough onto ungreased cookie sheets
        7. Bake for 10-12 minutes or until golden brown
        8. Cool on baking sheet for 2 minutes before removing

        Prep time: 20 minutes""",
    },
    {
        "name": "Simple Recipe (no prep time)",
        "text": """Avocado Toast: Take 1 ripe avocado, 2 slices bread, salt and pepper to taste. Toast the bread, mash the avocado, spread on toast, season with salt and pepper.""",
    },
    {
        "name": "Recipe with Ambiguous Quantities",
        "text": """Quick Smoothie Recipe: Blend together some frozen berries, a banana, yogurt (about a cup), and a splash of milk. Add honey if you want it sweeter. Blend until smooth and enjoy immediately. Takes about 5 minutes total.""",
    },
]

EVENT_EXAMPLES = [
    {
        "name": "Complete Event",
        "text": "Join us for the Annual Tech Conference on March 15, 2025 at the San Francisco Convention Center. Expected attendees include Sarah Chen, Michael Rodriguez, Dr. Emily Johnson, and over 500 industry professionals.",
    },
    {
        "name": "Minimal Event (no location or attendees)",
        "text": "Team standup meeting scheduled for tomorrow, January 10th at 9 AM.",
    },
    {
        "name": "Casual Event Description",
        "text": """Hey everyone! We're having a team building BBQ on Saturday, June 20th at Golden Gate Park.
        So far we have confirmations from: Alex, Jamie, Chris, Taylor, Morgan, and Sam.
        Bring your families! We'll have games, food, and fun starting at noon.""",
    },
]

SCHEMA_EXAMPLES = {
    "contact": CONTACT_EXAMPLES,
    "recipe": RECIPE_EXAMPLES,
    "event": EVENT_EXAMPLES,
}


def get_examples(schema_name: str) -> list[dict[str, str]]:
    return SCHEMA_EXAMPLES.get(schema_name, [])


def get_all_examples() -> dict[str, list[dict[str, str]]]:
    return SCHEMA_EXAMPLES
