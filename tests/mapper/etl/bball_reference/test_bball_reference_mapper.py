import pandas as pd 
import pytest 
from datetime import datetime 

from app.dto.etl.bball_reference.player_dto import PlayerDto
from app.dto.etl.bball_reference.roster_dto import RosterDto
from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper

GET_ROSTER_RESP_FILE = "./tests/data/etl/bball_reference/get_roster_response.json"
TEST_TEAM_IDENTIFIER = "CHI"
class TestBballReferenceMapper():
    
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
        self.mapper = BballReferenceMapper()
        self.team_name = TEST_TEAM_IDENTIFIER
        self.test_data = {
            "get_roster_response": pd.read_json(GET_ROSTER_RESP_FILE)
        }

    def test_get_team_from_df_returns_a_team_dto_when_given_valid_df(
        self,
        mapper,
        valid_df
    ):
        for _, row in valid_df.iterrows():
            team = mapper.get_team_from_df(row)
            assert team.name.lower() == row['EXPECTED_NAME'].lower()
            assert team.identifier.lower() == row['TEAM'].lower()
    
    def test_get_roster_from_df_returns_a_roster_dto_given_valid_df(self):
        df = self.test_data['get_roster_response']
        year = datetime.now().year 

        roster = self.mapper.get_roster_from_df(
            self.team_name,
            year,
            df 
        )

        assert(roster.season_end_year == year)
        assert(roster.season_start_year == year - 1)
        assert(roster.team_identifier == self.team_name)
        self._assert_players_equal_df(roster.players, df)

    def test_get_players_from_df_returns_a_list_of_player_dtos(self):
        df = self.test_data['get_roster_response']
        players = self.mapper.get_players_from_df(df)

        self._assert_players_equal_df(players, df)

    def test_get_team_name_by_identifier_raises_value_error_if_identifier_null(
        self,
        mapper
    ):
        with pytest.raises(
            ValueError, 
            match="Identifier cannot be None"
        ):
            mapper.get_team_name_by_identifier(None)

    def test_get_team_name_by_identifier_raises_value_error_if_identifier_is_not_valid(
        self,
        mapper
    ):
        invalid_name = "NOTANID"

        with pytest.raises(
            ValueError, 
            match=f"Team name: {invalid_name} not found."
        ):
            mapper.get_team_name_by_identifier(invalid_name)

    def test_get_team_name_by_identifier_returns_the_name_of_a_valid_team(
        self,
        mapper,
        valid_df
    ):
        mapper = BballReferenceMapper()

        for _, row in valid_df.iterrows():
            team_name = mapper.get_team_name_by_identifier(row['TEAM'])
            assert team_name == row['EXPECTED_NAME']

            team_name = mapper.get_team_name_by_identifier(row['TEAM'].lower())
            assert team_name == row['EXPECTED_NAME']


    def _assert_players_equal_df(
            self,
            players: list[PlayerDto], 
            df: pd.DataFrame
        ):
            assert(len(players) == len(df))

            for i in range(len(players)):
                assert players[i].first_name == df.iloc[i]['player'].split(" ")[0]
                assert players[i].last_name == df.iloc[i]['player'].split(" ")[1]
                assert players[i].number == df.iloc[i]['number']
                assert players[i].pos == df.iloc[i]['pos']
                assert players[i].height == df.iloc[i]['height']
                assert players[i].weight == df.iloc[i]['weight']
                assert players[i].birth_date == df.iloc[i]['birth_date']
                assert players[i].nationality == df.iloc[i]['nationality']
                assert players[i].college == df.iloc[i]['college']
