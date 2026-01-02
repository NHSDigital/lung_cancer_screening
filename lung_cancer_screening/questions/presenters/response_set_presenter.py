from decimal import Decimal

from ..models.respiratory_conditions_response import RespiratoryConditionValues

class ResponseSetPresenter:
    DATE_FORMAT = "%-d %B %Y" # eg 8 September 2000

    def __init__(self, response_set):
        self.response_set = response_set

    @property
    def have_you_ever_smoked(self):
        if not hasattr(self.response_set, 'have_you_ever_smoked_response'):
            return None

        return self.response_set.have_you_ever_smoked_response.get_value_display()

    @property
    def date_of_birth(self):
        if not hasattr(self.response_set, 'date_of_birth_response'):
            return None

        return self.response_set.date_of_birth_response.value.strftime(self.DATE_FORMAT)

    @property
    def height(self):
        if not hasattr(self.response_set, 'height_response'):
            return None

        if self.response_set.height_response.metric:
            return f"{Decimal(self.response_set.height_response.metric) / 10} cm"
        elif self.response_set.height_response.imperial:
            value = Decimal(self.response_set.height_response.imperial)
            return f"{value // 12} feet {value % 12} inches"
        else:
            return None

    @property
    def weight(self):
        if not hasattr(self.response_set, 'weight_response'):
            return None

        if self.response_set.weight_response.metric:
            return f"{Decimal(self.response_set.weight_response.metric) / 10} kg"
        elif self.response_set.weight_response.imperial:
            value = Decimal(self.response_set.weight_response.imperial)
            return f"{value // 14} stone {value % 14} pounds"
        else:
            return None

    @property
    def sex_at_birth(self):
        if not hasattr(self.response_set, 'sex_at_birth_response'):
            return None

        return self.response_set.sex_at_birth_response.get_value_display()

    @property
    def gender(self):
        if not hasattr(self.response_set, 'gender_response'):
            return None

        return self.response_set.gender_response.get_value_display()

    @property
    def ethnicity(self):
        if not hasattr(self.response_set, 'ethnicity_response'):
            return None

        return self.response_set.ethnicity_response.get_value_display()

    @property
    def asbestos_exposure(self):
        if not hasattr(self.response_set, 'asbestos_exposure_response'):
            return None

        return "Yes" if self.response_set.asbestos_exposure_response.value else "No"

    @property
    def cancer_diagnosis(self):
        if not hasattr(self.response_set, 'cancer_diagnosis_response'):
            return None

        return "Yes" if self.response_set.cancer_diagnosis_response.value else "No"

    @property
    def family_history_lung_cancer(self):
        if not hasattr(self.response_set, 'family_history_lung_cancer_response'):
            return None

        return self.response_set.family_history_lung_cancer_response.get_value_display()

    @property
    def respiratory_conditions(self):
        if not hasattr(self.response_set, 'respiratory_conditions_response'):
            return None

        return self._list_to_sentence([
            RespiratoryConditionValues(code).label
            for code in self.response_set.respiratory_conditions_response.value
        ])


    def _list_to_sentence(self, list):
        if len(list) == 0:
            return ''
        if len(list) == 1:
            return list[0]
        if len(list) == 2:
            return '{} and {}'.format(list[0], list[1])

        return '{}, and {}'.format(', '.join(list[:-1]), list[-1])
