from utils.load_config import load_service_config, load_timeout


def test_load_service_config():
    active_services = load_service_config()

    assert(type(active_services) == list)
    assert(type(active_services[0]) == str)
    assert "health" in active_services


def test_load_timeout():
    max_time = load_timeout()
    assert (type(max_time) == int)
    assert(60 > max_time > 0)
