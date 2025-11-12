import pytest

from app.dto.etl.bball_reference.team_dto import TeamDto
from app.service.etl.bball_reference.bball_reference_client import BballReferenceClient

class TestBballReferenceClient():
    def test_get_teams_returns_a_list_of_bball_ref_team_dto(self):
        client = BballReferenceClient()
        teams = client.get_teams()

        assert (len(teams) > 0)
        for team in teams:
            assert isinstance(type(team), type(TeamDto))