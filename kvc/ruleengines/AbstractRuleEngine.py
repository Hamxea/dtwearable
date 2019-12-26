from abc import ABC, abstractmethod


class AbstractRuleEngine(ABC):
    """ """

    @abstractmethod
    def execute(self, islem_dto, temperature, choosen_type, reference_table, reference_id, prediction_id):
        pass
