import pytest
from retry import retry

from exceptions import UnhealthyContainerException, HealthCheckFailedException
from consts import *

pytest_plugins = ["docker_compose"]

@retry(HealthCheckFailedException, delay=HEALTH_CHECKS_DELAY_SECS)
def wait_until_healthy(container):
    health_status = container.inspect()["State"]["Health"]["Status"]
    if health_status == "unhealthy":
        raise UnhealthyContainerException("Service is unhealthy")
    if not health_status == "healthy":
        raise HealthCheckFailedException()

def get_container_default_network_ip(container):
    default_network = container.project + "_default"
    networks = container.inspect()["NetworkSettings"]["Networks"]
    return container.inspect()["NetworkSettings"]["Networks"][default_network]["IPAddress"]

@pytest.fixture(scope="session")
def sql_server_service(request, docker_project, session_scoped_container_getter):
    container = session_scoped_container_getter.get("mysql-server")
    container_ip_address = get_container_default_network_ip(container)

    wait_until_healthy(container)

    return (container_ip_address,)



# Service configuration example
# import egg_shooter
#
#
# @pytest_fixture(scope="session")
# def egg_shooter_service():
#     service_container = session_scoped_container_getter.get("egg_shooter")
#     wait_until_healthy(service)
#
#     egg_shooter.configuration = EggShooterConfiguration(
#         ip = get_container_default_network_ip(service_container)
#     )
#
#     yield
#
#     # Tear down (such as removing files)
