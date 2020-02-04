class RuleViolationException(Exception):
    """ """

    message = None
    rule_enum = None
    value = None
    reference_table = None
    reference_id = None
    prediction_id = None

    def __init__(self, message, rule_enum, value, reference_table, reference_id, prediction_id):
        self.message = message
        self.rule_enum = rule_enum
        self.value = value
        self.reference_table = reference_table
        self.reference_id = reference_id
        self.prediction_id = prediction_id
