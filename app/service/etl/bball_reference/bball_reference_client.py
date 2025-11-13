from types import ModuleType
from datetime import datetime

import pandas as pd 
from basketball_reference_scraper import teams

from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper
from app.dto.etl.bball_reference.team_dto import TeamDto
from app.dto.etl.bball_reference.roster_dto import RosterDto

# TODO: datetime.now().year into util method for get current season
# TODO: separate out teams, roster, etc. into their own data providers
# TODO: add and apply validator methods for team and season end year
class BballReferenceClient():
    
    def __init__(self):
        self._set_teams_client(teams)
        self._set_roster_client(teams)
        self.mapper = BballReferenceMapper()

    # get player information:
    #   * for a specific team 
    #   * for the entire league for a year 
    #   * for all players over a specific period of time
    
    def get_teams(self, year: int = None) -> list:
        raw_teams = self.get_teams_raw(year)

        return list(raw_teams.apply(
            lambda row: self.mapper.get_team_from_df(row), axis=1
        ))
    
    def get_teams_raw(self, year: int = None) -> pd.DataFrame:
        if year is None:
            year = datetime.now().year

        return self._get_teams_client().get_team_ratings(year) 
        
    def get_roster(self, team: str, year: int = None) -> RosterDto:
        if year is None:
            year = datetime.now().year

        return self.mapper.get_roster_from_df(
            team,
            year,
            self.get_roster_raw(team, year)
        )

    def get_roster_raw(self, team: str, year: int = None) -> pd.DataFrame:
        if year is None:
            year = datetime.now().year

        return self._get_roster_client().get_roster(
            team, 
            year
        )
    
    # private 
    
    def _get_teams_client(self) -> ModuleType:
        return self.teams_client

    def _set_teams_client(self, teams):
        assert(hasattr(teams, ("get_team_ratings")))
        self.teams_client = teams

    def _get_roster_client(self) -> ModuleType:
        return self.roster_client

    def _set_roster_client(self, roster_client) -> None:
        assert(hasattr(roster_client, ("get_roster")))
        self.roster_client = roster_client