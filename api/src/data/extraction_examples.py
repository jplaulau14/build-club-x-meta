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

JOB_POSTING_EXAMPLES = [
    {
        "name": "Complete Job Posting",
        "text": """Senior Software Engineer at TechCorp Inc

Location: San Francisco, CA (Hybrid)
Salary: $140,000 - $180,000 per year
Job Type: Full-time
Experience Level: Senior

Description:
We are seeking an experienced Senior Software Engineer to join our growing engineering team. You'll be working on cutting-edge cloud infrastructure and building scalable microservices that serve millions of users daily.

Requirements:
- 5+ years of professional software development experience
- Strong proficiency in Python, Go, or Java
- Experience with AWS or GCP
- Bachelor's degree in Computer Science or related field
- Excellent problem-solving and communication skills

Posted: March 15, 2024""",
    },
    {
        "name": "Minimal Job Posting",
        "text": """Looking for a Marketing Manager at StartupXYZ. We need someone who can lead our marketing efforts and build our brand. Competitive salary. Apply today!""",
    },
    {
        "name": "Casual Job Description",
        "text": """We're hiring! Frontend Developer position open at Digital Agency Co in Austin, TX. Part-time contract work, $50-70/hr depending on experience. Must know React and TypeScript. Mid-level preferred. Email us your portfolio!""",
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

BUG_REPORT_EXAMPLES = [
    {
        "name": "Critical Bug with Full Details",
        "text": """URGENT: Payment Processing Failure

Description: The checkout process is completely broken. Users cannot complete purchases and we're losing revenue.

Steps to Reproduce:
1. Add items to cart
2. Proceed to checkout
3. Enter payment information
4. Click "Complete Purchase" button
5. Page freezes and then shows error

Expected Behavior: Payment should be processed successfully and order confirmation displayed.

Actual Behavior: Application freezes for 5-10 seconds, then displays "NullPointerException: Cannot read property 'amount' of undefined"

Environment: Chrome 120.0, Safari 17.1, Firefox 121.0 - affects all browsers
Version: 2.3.1 (production)
OS: Windows 11, macOS Ventura, iOS 17

Error Log:
```
NullPointerException at PaymentService.js:147
  at processPayment (PaymentService.js:147)
  at handleSubmit (CheckoutForm.js:89)
  at onClick (Button.js:23)
```

This is BLOCKING our Black Friday sales! We've had 50+ customer complaints in the last hour.""",
    },
    {
        "name": "Medium Severity UI Bug",
        "text": """Button alignment issue on mobile devices

When viewing the profile page on mobile (iPhone 14, Android Pixel 7), the "Save Changes" button is cut off at the bottom of the screen. Users have to scroll to see it, but scrolling doesn't work properly.

Steps:
1. Open app on mobile device
2. Navigate to Profile > Edit Profile
3. Try to click Save button

Expected: Button should be visible and clickable
Actual: Button is partially hidden below viewport

This affects version 1.8.2. Doesn't happen on desktop or tablet views. Several users reported this but there's a workaround - users can rotate device to landscape mode.

Labels: mobile, ui, css""",
    },
    {
        "name": "Low Priority Edge Case",
        "text": """Dark mode: tooltip text hard to read

In dark mode, tooltips that appear when hovering over icons have dark gray text on a black background, making them almost impossible to read.

To reproduce: Enable dark mode, hover over any info icon
Expected: Tooltip text should be readable
Actual: Text color blends with background

Found in v3.1.0. Only happens in dark mode. Light mode works fine. Very minor issue, most users probably won't notice.""",
    },
]

SCHEMA_EXAMPLES = {
    "contact": CONTACT_EXAMPLES,
    "job_posting": JOB_POSTING_EXAMPLES,
    "event": EVENT_EXAMPLES,
    "bug_report": BUG_REPORT_EXAMPLES,
}


def get_examples(schema_name: str) -> list[dict[str, str]]:
    return SCHEMA_EXAMPLES.get(schema_name, [])


def get_all_examples() -> dict[str, list[dict[str, str]]]:
    return SCHEMA_EXAMPLES
