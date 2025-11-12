from pandas import DataFrame
import pytest 

from app.mapper.etl.bball_reference.bball_reference_mapper import BballReferenceMapper

class TestBballReferenceMapper():
    
    @pytest.fixture
    def mapper(self):
        return BballReferenceMapper()
    
    @pytest.fixture
    def valid_df(self):
        return DataFrame({
            'TEAM': ['CHO', 'CHI'], 
            'EXPECTED_NAME': ['CHARLOTTE HORNETS', 'CHICAGO BULLS']
        })

    def test_get_team_from_df_returns_a_team_dto_when_given_valid_df(
        self,
        mapper,
        valid_df
    ):
        for _, row in valid_df.iterrows():
            team = mapper.get_team_from_df(row)
            assert team.name.lower() == row['EXPECTED_NAME'].lower()
            assert team.identifier.lower() == row['TEAM'].lower()
        
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


