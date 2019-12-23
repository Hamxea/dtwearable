from abc import ABC, abstractmethod


class AbstractRuleEngine(ABC):
    """ """

    @abstractmethod
    def execute(self, islem_dto, value):
        pass
