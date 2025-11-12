
from app.dto.etl.bball_reference.team_dto import TeamDto

class BballReferenceClient():
    def __init__(self):
        pass 

    def get_teams(self) -> list[TeamDto]:
        return [TeamDto()]