from app.constant.team import TEAM_TO_TEAM_ABBR
from app.dto.etl.bball_reference.team_dto import TeamDto
from app.dto.etl.bball_reference.roster_dto import RosterDto
from app.dto.etl.bball_reference.player_dto import PlayerDto
from pandas import DataFrame

class BballReferenceMapper:
    def __init__(self):
        self._set_team_map()

    def get_team_from_df(self, raw_team: DataFrame) -> TeamDto:
        return TeamDto(
            raw_team['TEAM'],
            self.get_team_name_by_identifier(raw_team['TEAM'])
        )

    def get_roster_from_df(
        self, 
        team_identifier: str,
        season_end_year: int,
        raw_players: DataFrame
    ) -> RosterDto:
        return RosterDto(
            team_identifier, 
            season_end_year, 
            self.get_players_from_df(raw_players)
        )

    def get_players_from_df(self, raw_players: DataFrame) -> list[PlayerDto]:
        raw_players.columns = map(str.lower, raw_players.columns)

        return raw_players.apply(
            lambda row: PlayerDto(**row), axis=1
        ).tolist()

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