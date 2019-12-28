from abc import ABC, abstractmethod


class AbstractRuleEngine(ABC):
    """ """

    @abstractmethod
    def execute(self, islem_dto, value, yas, tansiyon_sistolik, tansiyon_diastolik, choosen_type, reference_table, reference_id, prediction_id):
        pass
