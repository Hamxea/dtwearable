from ai.enums.PriorityEnum import PriorityEnum
from dt.ruleengines.AbstractRuleEngine import AbstractRuleEngine
from dt.ruleengines.RuleViolationException import RuleViolationException
from dt.ruleengines.enums.BloodPressureEnum import BloodPressureEnum
from dt.ruleengines.enums.ChoosenTypeEnum import ChoosenTypeEnum


class BloodPressureRuleEngine(AbstractRuleEngine):
    """ Reference: https://www.health.harvard.edu/heart-health/reading-the-new-blood-pressure-guidelines
    """

    def execute(self, value, age, blood_pressure_systolic, blood_pressure_diastolic, choosen_type, reference_table,
                reference_id, prediction_id, notification_id, priority):
        """ """

        exception_list = []

        if 120 <= blood_pressure_systolic <= 129 and blood_pressure_diastolic < 80:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("Temperature Rises: "
                                           "THE TENSION SYSTOLIC increased between 120 and 129"
                                           "and BP fell below DIASTOLIC 80",
                                           BloodPressureEnum.HIGH_BLOOD_PRESSURE, blood_pressure_systolic,
                                           reference_table,
                                           reference_id,
                                           prediction_id,
                                           notification_id, priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(
                    RuleViolationException("Tension May Rise: "
                                           "THE TENSION SYSTOLIC can go up between 120 and 129"
                                           "and BP may drop below DIASTOLIC 80",
                                           BloodPressureEnum.HIGH_BLOOD_PRESSURE, blood_pressure_systolic,
                                           reference_table,
                                           reference_id,
                                           prediction_id,
                                           notification_id, priority=PriorityEnum.MEDIUM))

        elif 130 <= blood_pressure_systolic <= 139 or 80 <= blood_pressure_diastolic <= 89:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException("Temperature Rises: "
                                                             "THE TENSION SYSTOlic is between 130 and 139"
                                                             "or BP increased between DIASTOLIC 89 and 80"
                                                             "(HYPERTENSION STEP-1)",
                                                             BloodPressureEnum.HIGH_BLOOD_PRESSURE_HYPERTENSION_STAGE_1,
                                                             blood_pressure_systolic, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))
            else:
                exception_list.append(RuleViolationException("Tension May Rise: "
                                                             "THE TENSION SYSTOLIC can go up between 130 and 139"
                                                             "or BP DIASTOLIC 89 to 80"
                                                             "(HYPERTENSION STEP-1)",
                                                             BloodPressureEnum.HIGH_BLOOD_PRESSURE_HYPERTENSION_STAGE_1,
                                                             blood_pressure_systolic, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))

        elif blood_pressure_systolic >= 140 or blood_pressure_diastolic > 90:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(RuleViolationException("Temperature Rises: "
                                                             "THE BLOOD PRESSURE SYSTOlic 140"
                                                             "or BP rises above DIASTOLIC 90"
                                                             "(HYPERTENSION STEP-2).",
                                                             BloodPressureEnum.HIGH_BLOOD_PRESSURE_HYPERTENSION_STAGE_2,
                                                             blood_pressure_systolic, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.HIGH))
            else:
                exception_list.append(RuleViolationException("Tension May Rise: "
                                                             "THE TENSION SYSTOLIC can go up between 130 and 139"
                                                             "or BP DIASTOLIC 89 to 80 (HYPERTENSION STEP-1)",
                                                             BloodPressureEnum.HIGH_BLOOD_PRESSURE_HYPERTENSION_STAGE_1,
                                                             blood_pressure_systolic, reference_table, reference_id,
                                                             prediction_id, notification_id,
                                                             priority=PriorityEnum.MEDIUM))

        elif blood_pressure_systolic >= 180 and blood_pressure_diastolic > 120:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("The Blood Pressure Is Too High: "
                                           "BLOOD TENSION SYSTOLIC rose above 180"
                                           "and BP rose above DIASTOLIC 120"
                                           "(HYPERTENSIVE CRISES)",
                                           BloodPressureEnum.HYPERTENSION_CRISIS,
                                           blood_pressure_systolic, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException("The Blood Pressure Can Get Too High"
                                           "THE BLOOD PRESSURE SYSTOLIC can rise above 180"
                                           "and BP may rise above DIASTOLIC 120"
                                           "(HYPERTENSIVE CRISES)",
                                           BloodPressureEnum.HYPERTENSION_CRISIS,
                                           blood_pressure_systolic, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))

        elif blood_pressure_systolic >= 180 or blood_pressure_diastolic > 120:
            if choosen_type == ChoosenTypeEnum.REAL:
                exception_list.append(
                    RuleViolationException("The Blood Pressure Is Too High: "
                                           "BLOOD TENSION SYSTOLIC rose above 180"
                                           "or BP rises above DIASTOLIC 120"
                                           "(HYPERTENSIVE CRISES)",
                                           BloodPressureEnum.HYPERTENSION_CRISIS,
                                           blood_pressure_systolic, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))
            else:
                exception_list.append(
                    RuleViolationException("The Blood Pressure Can Get Too High"
                                           "THE BLOOD PRESSURE SYSTOLIC MAY RISE TO 180"
                                           "or BP may rise above DIASTOLIC 120"
                                           "(HYPERTENSIVE CRISES)",
                                           BloodPressureEnum.HYPERTENSION_CRISIS,
                                           blood_pressure_systolic, reference_table, reference_id, prediction_id,
                                           notification_id, priority=PriorityEnum.HIGH))

        return exception_list
