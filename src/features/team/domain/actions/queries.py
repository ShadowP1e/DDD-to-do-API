from dataclasses import dataclass


@dataclass
class GetTeamQuery:
    id: int
    user_id: int


@dataclass
class GetTeamsWithUserQuery:
    user_id: int
