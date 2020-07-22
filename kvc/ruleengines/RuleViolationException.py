class RuleViolationException(Exception):
    """ """
    islem_no = None
    message = None
    rule_enum = None
    value = None
    reference_table = None
    reference_id = None
    prediction_id = None
    notification_id = None
    priority = None

    def __init__(self, islem_no, message, rule_enum, value, reference_table, reference_id, prediction_id,
                 notification_id, priority):
        self.islem_no = islem_no
        self.message = message
        self.rule_enum = rule_enum
        self.value = value
        self.reference_table = reference_table
        self.reference_id = reference_id
        self.prediction_id = prediction_id
        self.notification_id = notification_id
        self.priority = priority
