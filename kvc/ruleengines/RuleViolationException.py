
class RuleViolationException(Exception):
    """ """

    message = None
    rule_enum = None

    def __init__(self, message, rule_enum):
        self.message = message
        self.rule_enum = rule_enum
