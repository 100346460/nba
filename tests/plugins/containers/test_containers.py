"""Use to ensure that Airflow is setup correctly"""
from plugins.containers.podman import Podman
import pytest
import time

@pytest.fixture
def setup():
    Podman.machine_start()
    Podman.create_postgres_container(container_name="airflow-postgres",
                                     postgres_user="airflow",
                                     postgres_password="airflow",
                                     postgres_db="airflow",
                                     volumes="~/podman-volumes/airflow-postgres-data:/var/lib/postgresql/data",
                                     port=5438)
    Podman.run_airflow_migrate()
    Podman.run_airflow_webserver("airflow-webserver")
    Podman.run_airflow_scheduler("airflow-scheduler")
    time.sleep(5)
    yield
    #Podman.kill_all_containers()


def test_create_required_airflow_containers(setup):    
    assert Podman.container_exists("airflow-postgres")
    assert Podman.container_exists("airflow-webserver")
    assert Podman.container_exists("airflow-scheduler")

