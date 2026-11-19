class DIContainer:
    def __init__(self):
        self._services = {}

    def register(self, interface, instance):
        self._services[interface] = instance

    def resolve(self, interface):
        if interface not in self._services:
            raise Exception(f"Зависимость {interface} не зарегистрирована в DI-контейнере!")
        return self._services[interface]