from decimal import Decimal
from django.urls import reverse

from ..models.education_response import EducationValues
from ..models.respiratory_conditions_response import RespiratoryConditionValues
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues

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
    def education(self):
        if not hasattr(self.response_set, 'education_response'):
            return None

        return self._list_to_sentence([
            EducationValues(code).label
            for code in self.response_set.education_response.value
        ])

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
        if not hasattr(self.response_set, 'family_history_lung_cancer'):
            return None

        return self.response_set.family_history_lung_cancer.get_value_display()

    @property
    def relatives_age_when_diagnosed(self):
        if not hasattr(self.response_set, 'relatives_age_when_diagnosed'):
            return None

        return self.response_set.relatives_age_when_diagnosed.get_value_display()


    @property
    def respiratory_conditions(self):
        if not hasattr(self.response_set, 'respiratory_conditions_response'):
            return None

        return self._list_to_sentence([
            RespiratoryConditionValues(code).label
            for code in self.response_set.respiratory_conditions_response.value
        ])


    def eligibility_responses_items(self):
        return [
            self._check_your_answer_item(
                "Have you ever smoked tobacco?",
                self.have_you_ever_smoked,
                "questions:have_you_ever_smoked",
            ),
            self._check_your_answer_item(
                "Date of birth",
                self.date_of_birth,
                "questions:date_of_birth",
            )
        ]

    def about_you_responses_items(self):
        return [
            self._check_your_answer_item(
                "Height",
                self.height,
                "questions:height",
            ),
            self._check_your_answer_item(
                "Weight",
                self.weight,
                "questions:weight",
            ),
            self._check_your_answer_item(
                "Sex at birth",
                self.sex_at_birth,
                "questions:sex_at_birth",
            ),
            self._check_your_answer_item(
                "Gender identity",
                self.gender,
                "questions:gender",
            ),
            self._check_your_answer_item(
                "Ethnic background",
                self.ethnicity,
                "questions:ethnicity",
            ),
            self._check_your_answer_item(
                "Education",
                self.education,
                "questions:education",
            )
        ]


    def your_health_responses_items(self):
        return [
            self._check_your_answer_item(
                "Diagnosed respiratory conditions",
                self.respiratory_conditions,
                "questions:respiratory_conditions",
            ),
            self._check_your_answer_item(
                "Have you ever worked in a job where you were exposed to asbestos?",
                self.asbestos_exposure,
                "questions:asbestos_exposure",
            ),
            self._check_your_answer_item(
                "Have you ever been diagnosed with cancer?",
                self.cancer_diagnosis,
                "questions:cancer_diagnosis",
            )
        ]


    def family_history_responses_items(self):
        items = [
            self._check_your_answer_item(
                "Have any of your parents, siblings or children ever been diagnosed with lung cancer?",
                self.family_history_lung_cancer,
                "questions:family_history_lung_cancer",
            )
        ]
        if self._should_display_relatives_age_when_diagnosed():
            items.append(self._check_your_answer_item(
                "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?",
                self.relatives_age_when_diagnosed,
                "questions:relatives_age_when_diagnosed",
            ))

        return items


    def _list_to_sentence(self, list):
        if len(list) == 0:
            return ''
        if len(list) == 1:
            return list[0]
        if len(list) == 2:
            return '{} and {}'.format(list[0], list[1])

        return '{}, and {}'.format(', '.join(list[:-1]), list[-1])


    def _should_display_relatives_age_when_diagnosed(self):
        if not hasattr(self.response_set, 'family_history_lung_cancer'):
            return False

        return self.response_set.family_history_lung_cancer != FamilyHistoryLungCancerValues.YES


    def _change_query_params(self):
        return { "change": "True" }


    def _check_your_answer_item(self, question, value, url_lookup_name):
        return {
            "key": { "text": question },
            "value": { "text": value },
            "actions": {
                "items": [
                    {
                        "href": reverse(url_lookup_name, query = self._change_query_params()),
                        "text": "Change"
                    }
                ]
            }
        }
