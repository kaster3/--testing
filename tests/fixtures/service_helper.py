import pytest

from app.service_layer.service_helper import ServiceHelper


@pytest.fixture()
def service_helper() -> ServiceHelper:
    return ServiceHelper()
