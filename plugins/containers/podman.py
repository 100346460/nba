import subprocess
import json

class Podman:
    @classmethod
    def machine_start(cls) -> None:
        """Runs as podman-machine-default"""
        result = subprocess.run(["podman", "machine", "start"],   
                           stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        if result.returncode == 125:
            print("Machine already started, proceeding.")
            return
        if result.returncode != 0:
            raise EnvironmentError(f"Podman machine failing: {result.stderr} value {result.returncode}")


    @classmethod
    def container_exists(cls, container_name: str) -> bool:
        result = subprocess.run(
        ["podman", "container", "exists", container_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
        if result.returncode != 0:
            return False
        return True
    
    @classmethod
    def create_postgres_container(cls,
                                  container_name: str,
                                  postgres_user: str,
                                  postgres_password: str,
                                  postgres_db: str,
                                  port: int,
                                  volumes: str = ""):
        """
        Runs a Podman container for PostgreSQL with the specified configuration.
        """
        command = f"""podman run -d \
--name {container_name} \
-e POSTGRES_USER={postgres_user} \
-e POSTGRES_PASSWORD={postgres_password} \
-e POSTGRES_DB={postgres_db} \
-v {volumes} \
-p {port}:5432 \
postgres:15"""
        if not volumes:
            command = command.replace("-v","")
        if not Podman.container_exists(container_name):
            subprocess.run(command, shell=True, check=True, executable="/bin/bash")

    @classmethod
    def run_airflow_migrate(cls):
        command = """podman run -d --env-file .env my-airflow airflow db migrate"""
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")

    @classmethod
    def run_airflow_webserver(cls, container_name: str):
        command = f"""podman run -d --env-file .env \
-v ~/airflow-logs:/opt/airflow/logs \
-v /Users/mathieucardinal/repos/pga/dags:/opt/airflow/dags \
-v /Users/mathieucardinal/repos/pga/plugins:/opt/airflow/plugins \
-p 8080:8080 \
--name {container_name} \
my-airflow airflow webserver"""
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")

    @classmethod
    def run_airflow_scheduler(cls, container_name: str):
        command = f"""podman run -d --env-file .env \
-v ~/airflow-logs:/opt/airflow/logs \
-v /Users/mathieucardinal/repos/pga/dags:/opt/airflow/dags \
-v /Users/mathieucardinal/repos/pga/plugins:/opt/airflow/plugins \
--name {container_name} \
my-airflow airflow scheduler"""
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")

    @classmethod
    def kill_postgres_container(cls,
                                container_name: str):
        subprocess.run([f"podman kill {container_name} || true"], shell=True, check=True, executable="/bin/bash")
        subprocess.run([f"podman rm {container_name} || true"], shell=True, check=True, executable="/bin/bash")

    @classmethod
    def kill_all_containers(cls):
        subprocess.run([f"podman kill $(podman ps -q) || true"], shell=True, check=True, executable="/bin/bash")
        subprocess.run([f"podman rm $(podman ps -aq) || true"], shell=True, check=True, executable="/bin/bash")
