from custom_observer import CustomObserver


class CustomObservable:
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        if not isinstance(observer, CustomObserver):
            raise ValueError("Illegal observer class: " + str(type(observer)) + ".")
        else:
            self.__add_observer_if_needed(observer)

    def __add_observer_if_needed(self, observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def get_observers(self):
        return self.__observers

    def get_specific_type_observers(self, specific_class):
        return [x for x in self.__observers and isinstance(x, specific_class)]

    def notify_observers(self, payload):
        for observer in self.__observers:
            observer.update(self, payload)

    def notify_specific_type_observers(self, payload, specific_class):
        for observer in self.get_specific_type_observers(specific_class):
            observer.update(self, payload)
