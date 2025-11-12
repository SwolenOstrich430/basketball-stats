from app.constant.team import TEAM_TO_TEAM_ABBR
from app.dto.etl.bball_reference.team_dto import TeamDto
from pandas import DataFrame

class BballReferenceMapper:
    def __init__(self):
        self._set_team_map()

    def get_team_from_df(self, raw_team: DataFrame) -> TeamDto:
        return TeamDto(
            raw_team['TEAM'],
            self.get_team_name_by_identifier(raw_team['TEAM'])
        )

    def get_team_name_by_identifier(self, identifier: str) -> str:
        if identifier is None:
            raise ValueError("Identifier cannot be None.")

        formatted_identifier = identifier.lower()

        if formatted_identifier not in self._get_team_map():
            raise ValueError(f"Team name: {identifier} not found.")

        return self._get_team_map()[formatted_identifier]
    
    def _get_team_map(self) -> dict[str, str]:
        return self.team_map

    def _set_team_map(self):
        self.team_map = {
            value.lower(): key for key, value in TEAM_TO_TEAM_ABBR.items()
        }