from decimal import Decimal, getcontext

getcontext().prec = 999999

class Plco:
    AGE_COEFFICIENT = Decimal('0.0778868')
    AGE_CENTRED_OR_REFERENT_REF_GROUP = Decimal('62')
    BMI_COEFFICIENT = Decimal('-0.0274194')
    BMI_CENTRED_OR_REFERENT_REF_GROUP = Decimal('27')
    COPD_ENPHYSEMA_OR_CHRONIC_BRONCHITIS_COEFFICIENT = Decimal('0.3553063')
    PERSONAL_HISTORY_OF_CANCER_COEFFICIENT = Decimal('0.4589971')
    FAMILY_HISTORY_OF_CANCER_COEFFICIENT = Decimal('0.587185')

    def __init__(self,
                 age,
                 bmi,
                 copd_enphysema_or_chronic_bronchitis,
                 personal_history_of_cancer,
                 family_history_of_cancer):
        self.age = Decimal(str(age or 0))
        self.bmi = Decimal(str(bmi or 0))
        self.copd_enphysema_or_chronic_bronchitis = copd_enphysema_or_chronic_bronchitis
        self.personal_history_of_cancer = personal_history_of_cancer
        self.family_history_of_cancer = family_history_of_cancer

    def age_in_years_contribution_to_estimate(self):
        return (self.age - self.AGE_CENTRED_OR_REFERENT_REF_GROUP) * self.AGE_COEFFICIENT

    def bmi_contribution_to_estimate(self):
        return (self.bmi - self.BMI_CENTRED_OR_REFERENT_REF_GROUP) * self.BMI_COEFFICIENT

    def copd_enphysema_or_chronic_bronchitis_contribution_to_estimate(self):
        if self.copd_enphysema_or_chronic_bronchitis is None:
            raise self.InvalidValueError(
                "copd_enphysema_or_chronic_bronchitis must be set")

        return self.copd_enphysema_or_chronic_bronchitis * self.COPD_ENPHYSEMA_OR_CHRONIC_BRONCHITIS_COEFFICIENT


    def personal_history_of_cancer_contribution_to_estimate(self):
        if self.personal_history_of_cancer is None:
            raise self.InvalidValueError(
                "personal_history_of_cancer must be set")

        return self.personal_history_of_cancer * self.PERSONAL_HISTORY_OF_CANCER_COEFFICIENT

    def family_history_of_cancer_contribution_to_estimate(self):
        if self.family_history_of_cancer is None:
            raise self.InvalidValueError(
                "family_history_of_cancer must be set")

        return self.family_history_of_cancer * self.FAMILY_HISTORY_OF_CANCER_COEFFICIENT

    class InvalidValueError(Exception):
        pass
