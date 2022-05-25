from abc import ABC, abstractmethod


class AbstractRuleEngine(ABC):
    """ """

    @abstractmethod
    def execute(self, value, age, blood_pressure_systolic, blood_pressure_diastolic, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        pass
