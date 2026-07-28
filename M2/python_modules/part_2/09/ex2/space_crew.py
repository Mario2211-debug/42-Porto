from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class Rank(Enum):
    cadet = "Cadet"
    officer = "Officer"
    lieutenant = "Lieutenant"
    capitan = "Capitan"
    commander = "Commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_rules(self):
        valid = []
        if not self.mission_id.startswith("M"):
            raise ValueError("")
        for member in self.crew:
            if member.rank == Rank.capitan or member.rank == Rank.commander:
                valid.append(member)
            if not member.is_active:
                raise ValueError("All members must be active")
            if self.duration_days > 365 and member.years_experience < 5:
                raise ValueError("For 1 year missions or more, members must"
                                 " have at least 5 years of experience.")
        if len(valid) == 0:
            raise ValueError("Mission must have at least "
                             "one Commander or Captain")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2026, 8, 10, 7, 30),
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="C01",
                name="Sarah Connor",
                rank=Rank.commander,
                age=41,
                specialization="Mission Command",
                years_experience=15,
            ),
            CrewMember(
                member_id="C02",
                name="John Smith",
                rank=Rank.lieutenant,
                age=35,
                specialization="Navigation",
                years_experience=7,
            ),
            CrewMember(
                member_id="C03",
                name="Alice Johnson",
                rank=Rank.officer,
                age=32,
                specialization="Engineering",
                years_experience=6,
            ),
        ],
    )
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) -"
              f" {member.specialization}")
    print("=========================================")
    try:
        SpaceMission(
            mission_id="MFAIL01",
            mission_name="Unsafe Survey",
            destination="Moon",
            launch_date=datetime(2026, 8, 10, 7, 30),
            duration_days=12,
            budget_millions=15.0,
            crew=[
                CrewMember(
                    member_id="A13",
                    name="Bob Ray",
                    rank=Rank.officer,
                    age=28,
                    specialization="Science",
                    years_experience=2,
                )
            ],
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
