import pytest
from unittest.mock import patch
from types import ModuleType
from datetime import datetime 

from pandas import DataFrame
from basketball_reference_scraper import teams


from app.dto.etl.bball_reference.team_dto import TeamDto
from app.service.etl.bball_reference.bball_reference_client import BballReferenceClient

class TestBballReferenceClient():
    def setup_method(self):
        self.client =  BballReferenceClient()

    def test_get_teams_returns_a_list_of_bball_ref_team_dto(self):
        teams = self.client.get_teams()

        assert (len(teams) > 0)

        for team in teams:
            assert isinstance(type(team), type(TeamDto))

    def test_get_teams_raw_returns_teams_for_the_current_year_if_year_is_null(self, mocker):
        mock_df = mocker.Mock()
        mock_team_client = mocker.Mock()
        mock_team_client.get_team_ratings.return_value = mock_df

        mocker.patch.object(
            self.client, 
            '_get_teams_client', 
            return_value=mock_team_client
        )

        ret_val = self.client.get_teams_raw()
        mock_team_client.get_team_ratings.assert_called_with(
            datetime.now().year
        )
        assert ret_val == mock_df