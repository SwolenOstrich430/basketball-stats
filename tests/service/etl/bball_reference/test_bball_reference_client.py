import pytest
from datetime import datetime 
 
import pandas as pd 
from basketball_reference_scraper import teams

from app.dto.etl.bball_reference.team_dto import TeamDto
from app.dto.etl.bball_reference.roster_dto import RosterDto
from app.service.etl.bball_reference.bball_reference_client import BballReferenceClient
from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper

GET_ROSTER_RESP_FILE = "./tests/data/etl/bball_reference/get_roster_response.json"
TEST_TEAM_IDENTIFIER = "CHI"
class TestBballReferenceClient():

    def refresh_test_data(self):
        df = teams.get_roster(TEST_TEAM_IDENTIFIER, datetime.now().year)
        df.to_json(GET_ROSTER_RESP_FILE, indent=4) 

    @pytest.fixture
    def mapper(self):
        return BballReferenceMapper()
    
    @pytest.fixture
    def valid_df(self):
        return pd.DataFrame({
            'TEAM': ['CHO', 'CHI'], 
            'EXPECTED_NAME': ['CHARLOTTE HORNETS', 'CHICAGO BULLS']
        })

    def setup_method(self):
        self.client =  BballReferenceClient()
        self.team_name = "CHI"
        self.test_data = {
            "get_roster_response": pd.read_json(GET_ROSTER_RESP_FILE)
        }

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

    def test_get_roster_returns_a_roster_dto(self, mocker):
        mocked_method = mocker.patch.object(
            self.client,
            'get_roster_raw',
            return_value=self.test_data['get_roster_response']
        )

        expected_roster = self.client.get_roster(
            self.team_name, 
            datetime.now().year
        )

        assert isinstance(type(expected_roster), type(RosterDto))
        mocked_method.assert_called_with(
            self.team_name, 
            datetime.now().year
        )
        
    def test_get_roster_raw_returns_a_data_frame(self, mocker): 
        mock_client = mocker.Mock()
        mock_client.get_roster.return_value = self.test_data['get_roster_response']
        
        mocker.patch.object(
            self.client,
            '_get_roster_client',
            return_value=mock_client
        )

        df = self.client.get_roster_raw(self.team_name)

        assert(len(df) > 0)
        assert isinstance(type(df), type(pd.DataFrame))

    def test_get_roster_raw_uses_current_season_if_supplied_is_null(self, mocker):
        mock_client = mocker.Mock()
        mock_client.get_roster.return_value = self.test_data['get_roster_response']
        
        mocker.patch.object(
            self.client,
            '_get_roster_client',
            return_value=mock_client
        )

        df = self.client.get_roster_raw(self.team_name)

        mock_client.get_roster.assert_called_with(
            TEST_TEAM_IDENTIFIER, 
            datetime.now().year
        )

        assert(len(df) > 0)
        assert isinstance(type(df), type(pd.DataFrame))