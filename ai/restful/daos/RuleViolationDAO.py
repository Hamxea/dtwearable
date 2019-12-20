from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.RuleViolationDTO import RuleViolationDTO


class RuleViolationDAO(AbstractDAO):
    """
    RuleViolation nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def __init__(self):
        super().__init__(RuleViolationDTO)

