from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
from typing import Optional


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if ContactType.telepathic and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at"
                             " least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals should include received messages")
        return self


def main() -> None:
    print("Space Station Data Validator")
    print("========================================")
    contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 4, 30),
            contact_type=ContactType.radio,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True,
    )
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.name}")
    print(f"Location: {contact.location} people")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")
    print("========================================")
    try:
        AlienContact(
            contact_id="AC_BAD_001",
            timestamp=datetime(2026, 4, 30),
            contact_type=ContactType.telepathic,
            location="Orbit",
            signal_strength=8.5,
            duration_minutes=5,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
            )
    except ValidationError as error:
        print("Excepted validation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
