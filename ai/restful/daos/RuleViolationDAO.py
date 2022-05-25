from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO


class RuleViolationDAO(AbstractDAO):
    """
    Contains the methods by which database operations are performed for the RuleViolation object
    """

    def __init__(self):
        super().__init__(RuleViolationDTO)

