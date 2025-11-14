import pytest
from datetime import datetime 
import json  
import pandas as pd 
from basketball_reference_scraper import teams
from basketball_reference_scraper import seasons
from basketball_reference_scraper import box_scores

from app.constant.team import TEAM_TO_TEAM_ABBR
from app.dto.etl.bball_reference.team_dto import TeamDto
from app.dto.etl.bball_reference.roster_dto import RosterDto
from app.service.etl.bball_reference.bball_reference_client import BballReferenceClient
from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper
from app.dto.etl.bball_reference.game_dto import GameDto
from app.dto.etl.bball_reference.box_score_dto import BoxScoreDto

GET_ROSTER_RESP_FILE = "./tests/data/etl/bball_reference/get_roster_response.json"
GET_SCHEDULE_RESPONSE = "./tests/data/etl/bball_reference/get_schedule_response.json"
GET_BOX_SCORE_RESPONSE_HOME = "./tests/data/etl/bball_reference/get_box_score_response_home.json"
GET_BOX_SCORE_RESPONSE_AWAY = "./tests/data/etl/bball_reference/get_box_score_response_away.json"
TEST_TEAM_IDENTIFIER = "CHI"
class TestBballReferenceClient():

    def refresh_test_data(self):
        df = teams.get_roster(TEST_TEAM_IDENTIFIER, datetime.now().year)
        df.to_json(GET_ROSTER_RESP_FILE, indent=4) 

        df1 = seasons.get_schedule(datetime.now().year)
        df1.to_json(GET_SCHEDULE_RESPONSE, indent=4)

        date = df1.iloc[0]['DATE']
        home_team = df1.iloc[0]['HOME'].upper()
        away_team = df1.iloc[0]['VISITOR'].upper()

        home_team_identifier = TEAM_TO_TEAM_ABBR[home_team]
        away_team_identifier = TEAM_TO_TEAM_ABBR[away_team]

        df3 = box_scores.get_box_scores(
            date, home_team_identifier, away_team_identifier
        )
        df3[home_team_identifier].to_json(GET_BOX_SCORE_RESPONSE_HOME, indent=4)
        df3[away_team_identifier].to_json(GET_BOX_SCORE_RESPONSE_AWAY, indent=4)


    @pytest.fixture
    def valid_df(self):
        return pd.DataFrame({
            'TEAM': ['CHO', 'CHI'], 
            'EXPECTED_NAME': ['CHARLOTTE HORNETS', 'CHICAGO BULLS']
        })

    def setup_method(self):
        # self.refresh_test_data()
        self.client =  BballReferenceClient()
        self.team_name = "CHI"
        self.test_data = {
            "get_roster_response": pd.read_json(GET_ROSTER_RESP_FILE),
            "get_schedule_response": pd.read_json(GET_SCHEDULE_RESPONSE),
            "get_box_score_response": {}
        }

        df1 = self.test_data["get_schedule_response"]
        self.date = df1.iloc[0]['DATE']
        self.home_team = df1.iloc[0]['HOME'].upper()
        self.away_team = df1.iloc[0]['VISITOR'].upper()
        self.home_team_identifier = TEAM_TO_TEAM_ABBR[self.home_team]
        self.away_team_identifier = TEAM_TO_TEAM_ABBR[self.away_team]

        self.test_data["get_box_score_response"][self.home_team_identifier] = pd.read_json(
            GET_BOX_SCORE_RESPONSE_HOME
        )
        self.test_data["get_box_score_response"][self.away_team_identifier] = pd.read_json(
            GET_BOX_SCORE_RESPONSE_AWAY
        )


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

    def test_get_season_returns_a_list_of_game_dtos(self, mocker):
        df = self.test_data['get_schedule_response']

        mocker.patch.object(
            self.client,
            'get_schedule_raw',
            return_value=df
        )

        game_dtos = self.client.get_season_schedule(
            datetime.now().year
        )

        assert(len(game_dtos) == len(df))

        for i in range(len(game_dtos)):
            assert(game_dtos[i].matchup.home_team_name == df.iloc[i]['HOME'])
            assert(game_dtos[i].matchup.away_team_name == df.iloc[i]['VISITOR'])
            assert(game_dtos[i].start_time == df.iloc[i]['DATE'])
            
    def test_get_season_raw_returns_a_data_frame(self, mocker):
        year = datetime.now().year 
        mock_client = mocker.Mock()
        mock_client.get_schedule.return_value = self.test_data['get_schedule_response']
        
        mocker.patch.object(
            self.client,
            '_get_season_client',
            return_value=mock_client
        )

        df = self.client.get_schedule_raw(year)

        assert isinstance(type(df), type(pd.DataFrame))
        assert df.equals(self.test_data['get_schedule_response'])
        mock_client.get_schedule.assert_called_with(year)

    def test_get_box_score_returns_a_box_score_dto(self, mocker):
        mock_client = mocker.Mock()

        mock_client.get_box_scores.return_value = self.test_data['get_box_score_response']

        mocker.patch.object(
            self.client,
            '_get_stats_client',
            return_value=mock_client
        )

        game = GameDto(
            start_time=self.date, 
            home_team_name=self.home_team,
            away_team_name=self.away_team,
            home_team_identifier=self.home_team_identifier, 
            away_team_identifier=self.away_team_identifier
        )

        box_score = self.client.get_box_score(game)
        assert isinstance(type(box_score), type(BoxScoreDto))

    def test_get_box_score_raw_returns_a_dict_with_teams_as_keys_and_box_scores_as_data_frames(
        self, 
        mocker
    ):
        mock_client = mocker.Mock()
        mock_client.get_box_scores.return_value = self.test_data['get_box_score_response']
        
        mocker.patch.object(
            self.client,
            '_get_stats_client',
            return_value=mock_client
        )

        df = self.client.get_box_score_raw(
            self.date, 
            self.home_team_identifier, 
            self.away_team_identifier
        )

        assert isinstance(type(df), type(dict))
        assert(self.home_team_identifier in df)
        assert(self.away_team_identifier in df)
        assert(isinstance(type(df[self.home_team_identifier]), type(pd.DataFrame)))
        assert(isinstance(type(df[self.away_team_identifier]), type(pd.DataFrame)))
        
        mock_client.get_box_scores.assert_called_with(
            self.date, 
            self.home_team_identifier, 
            self.away_team_identifier
        )