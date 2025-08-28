from django.test import TestCase
from decimal import Decimal

from lung_cancer_screening.calculators.plco import Plco

class TestPlco(TestCase):
    def test_age_in_years_contribution_to_estimate_when_age_is_none(self):
        calculator = Plco(age=None)
        result = calculator.age_in_years_contribution_to_estimate()

        self.assertEqual(result, Decimal('-4.8289816'))

    def test_age_in_years_contribution_to_estimate_at_74(self):
        calculator = Plco(age=74)
        result = calculator.age_in_years_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.9346416'))

    def test_age_in_years_contribution_to_estimate_at_62(self):
        calculator = Plco(age=58)
        result = calculator.age_in_years_contribution_to_estimate()

        self.assertEqual(result, Decimal('-0.3115472'))

    def test_bmi_contribution_to_estimate_when_bmi_is_none(self):
        calculator = Plco(bmi=None)
        result = calculator.bmi_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.7403238'))

    def test_bmi_contribution_to_estimate_when_bmi_is_23_point_5(self):
        calculator = Plco(bmi=23.5)
        result = calculator.bmi_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.0959679'))

    def test_bmi_contribution_to_estimate_when_bmi_is_a_long_decimal(self):
        calculator = Plco(bmi="26.4749212")
        result = calculator.bmi_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.01439734564872'))
