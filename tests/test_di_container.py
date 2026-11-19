import pytest
from infrastructure.di_container import DIContainer


class TestDIContainer:
    def test_register_and_resolve(self):
        c = DIContainer()
        obj = object()
        c.register("test", obj)
        assert c.resolve("test") is obj

    def test_resolve_unknown_raises(self):
        c = DIContainer()
        with pytest.raises(Exception, match="не зарегистрирована"):
            c.resolve("missing")