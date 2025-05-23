import pytest
from plugins.repositories.postgres import Postgres, create_teams_table, create_players_table, insert_players, insert_teams
from plugins.containers.podman import Podman
import time

@pytest.fixture
def golden_state_values() -> tuple:
    golden_state = {
        "id":10,
      "conference": "West",
    "division": "Pacific",
    "city": "Golden State",
    "name": "Warriors",
    "full_name": "Golden State Warriors",
    "abbreviation": "GSW"
    }
    return [tuple(golden_state.values())]

@pytest.fixture
def steph_curry_values() -> tuple:
    steph_curry = {
        "id": 19,
        "first_name": "Stephen",
        "last_name": "Curry",
        "position": "G",
        "height": "6-2",
        "weight": "185",
        "jersey_number": "30",
        "college": "Davidson",
        "country": "USA",
        "draft_year": 2009,
        "draft_round": 1,
        "draft_number": 7,
        "team_id": 10,
    }
    return [tuple(steph_curry.values())]

@pytest.fixture
def setup():
    Podman.create_postgres_container(
        container_name="test_nba_database",
        postgres_user="nba",
        postgres_db="nba",
        postgres_password="nba",
        port=5433
    )    
    time.sleep(1)
    yield
    Podman.kill_all_containers()


def test_nba_database(setup, golden_state_values, steph_curry_values):
    #basic database test
    with Postgres(dbname="nba",
                  user="nba",
                  password="nba",
                  host="localhost",
                  port=5433) as cursor:
        create_teams_table(cursor)
        insert_teams(cursor, golden_state_values)
        cursor.execute("SELECT COUNT(ID) FROM teams;")
        team_count = cursor.fetchone()[0]
        print(team_count)
        create_players_table(cursor)
        insert_players(cursor, steph_curry_values)
        cursor.execute("SELECT COUNT(ID) FROM players;")
        players_count = cursor.fetchone()[0]
        assert team_count == 1
        assert players_count == 1
    