from types import ModuleType
from datetime import datetime

from basketball_reference_scraper import teams
from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper
from app.dto.etl.bball_reference.team_dto import TeamDto

class BballReferenceClient():
    def __init__(self):
        self._set_teams_client(teams)
        self.mapper = BballReferenceMapper()

    def get_teams(self, year: int = None) -> list:
        raw_teams = self.get_teams_raw(year)
        
        return list(raw_teams.apply(
            lambda row: self.mapper.get_team_from_df(row), axis=1
        ))
    
    def get_teams_raw(self, year: int = None) -> list:
        if year is None:
            year = datetime.now().year

        return self._get_teams_client().get_team_ratings(year) 
        
    
    # private 
    
    # @classmethod 
    def _get_teams_client(self) -> ModuleType:
        return self.teams_client

    @classmethod
    def _set_teams_client(self, teams):
        assert(hasattr(teams, ("get_team_ratings")))
        self.teams_client = teams