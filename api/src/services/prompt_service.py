from datetime import datetime

from jinja2 import Template

LLAMA_PROMPT_TEMPLATE = Template(
    """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{% if include_knowledge_cutoff -%}
Cutting Knowledge Date: December 2023
Today Date: {{ current_date }}

{% endif -%}
{{ system_prompt }}<|eot_id|>
{%- for message in messages %}
<|start_header_id|>{{ message.role }}<|end_header_id|>

{{ message.content }}<|eot_id|>
{%- endfor %}
<|start_header_id|>assistant<|end_header_id|>

"""
)


def format_llama_prompt(
    system_prompt: str,
    messages: list[dict[str, str]] | None = None,
    include_knowledge_cutoff: bool = True,
) -> str:
    """Format messages in Llama 3.2 prompt format with special tokens."""
    return LLAMA_PROMPT_TEMPLATE.render(
        system_prompt=system_prompt,
        messages=messages or [],
        include_knowledge_cutoff=include_knowledge_cutoff,
        current_date=datetime.now().strftime("%d %B %Y"),
    )


def format_system_prompt(system_prompt: str) -> str:
    """Format system prompt with knowledge cutoff and current date."""
    return format_llama_prompt(
        system_prompt, messages=None, include_knowledge_cutoff=True
    )
