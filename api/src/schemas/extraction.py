from typing import Any, Literal

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None


class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str | None = None


class Recipe(BaseModel):
    title: str
    ingredients: list[Ingredient]
    instructions: list[str]
    prep_time: str | None = None


class Event(BaseModel):
    name: str
    date: str
    location: str | None = None
    attendees: list[str] = Field(default_factory=list)


class BugReport(BaseModel):
    title: str
    description: str
    steps_to_reproduce: list[str]
    expected_behavior: str
    actual_behavior: str
    severity: Literal["low", "medium", "high", "critical"]
    environment: str | None = None
    affected_version: str | None = None
    labels: list[str] = Field(default_factory=list)
    error_logs: str | None = None


class ExtractionRequest(BaseModel):
    text: str
    schema_name: str


class ExtractionResponse(BaseModel):
    data: dict[str, Any]
    schema_used: str


SCHEMA_REGISTRY: dict[str, type[BaseModel]] = {
    "contact": ContactInfo,
    "recipe": Recipe,
    "event": Event,
    "bug_report": BugReport,
}


def get_schema(schema_name: str) -> type[BaseModel] | None:
    return SCHEMA_REGISTRY.get(schema_name)
