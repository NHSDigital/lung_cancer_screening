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

    def test_copd_enphysema_or_chronic_bronchitiscontribution_to_estimate_when_none(self):
        calculator = Plco(copd_enphysema_or_chronic_bronchitis=None)

        self.assertRaises(
            Plco.InvalidValueError,
            calculator.copd_enphysema_or_chronic_bronchitis_contribution_to_estimate
        )

    def test_copd_enphysema_or_chronic_bronchitiscontribution_to_estimate_when_true(self):
        calculator = Plco(copd_enphysema_or_chronic_bronchitis=True)

        result = calculator.copd_enphysema_or_chronic_bronchitis_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.3553063'))

    def test_copd_enphysema_or_chronic_bronchitiscontribution_to_estimate_when_false(self):
        calculator = Plco(copd_enphysema_or_chronic_bronchitis=False)

        result = calculator.copd_enphysema_or_chronic_bronchitis_contribution_to_estimate()

        self.assertEqual(result, Decimal('0'))

    def test_personal_history_of_cancer_contribution_to_estimate_when_none(self):
        calculator = Plco(personal_history_of_cancer=None)

        self.assertRaises(
            Plco.InvalidValueError,
            calculator.personal_history_of_cancer_contribution_to_estimate
        )

    def test_personal_history_of_cancer_contribution_to_estimate_when_true(self):
        calculator = Plco(personal_history_of_cancer=True)

        result = calculator.personal_history_of_cancer_contribution_to_estimate()

        self.assertEqual(result, Decimal('0.4589971'))

    def test_personal_history_of_cancer_contribution_to_estimate_when_false(self):
        calculator = Plco(personal_history_of_cancer=False)

        result = calculator.personal_history_of_cancer_contribution_to_estimate()

        self.assertEqual(result, Decimal('0'))
