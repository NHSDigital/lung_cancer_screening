from decimal import Decimal, getcontext

getcontext().prec = 999999

class Plco:
    AGE_COEFFICIENT = Decimal('0.0778868')
    AGE_CENTRED_OR_REFERENT_REF_GROUP = Decimal('62')
    BMI_COEFFICIENT = Decimal('-0.0274194')
    BMI_CENTRED_OR_REFERENT_REF_GROUP = Decimal('27')

    def __init__(self, age=None, bmi=None):
        self.age = Decimal(str(age or 0))
        self.bmi = Decimal(str(bmi or 0))

    def age_in_years_contribution_to_estimate(self):
        return (self.age - self.AGE_CENTRED_OR_REFERENT_REF_GROUP) * self.AGE_COEFFICIENT

    def bmi_contribution_to_estimate(self):
        return (self.bmi - self.BMI_CENTRED_OR_REFERENT_REF_GROUP) * self.BMI_COEFFICIENT
