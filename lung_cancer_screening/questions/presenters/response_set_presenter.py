from decimal import Decimal
from django.urls import reverse
from inflection import dasherize, singularize

from ..models.respiratory_conditions_response import RespiratoryConditionValues
from ..models.education_response import EducationValues
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
from ..models.tobacco_smoking_history import TobaccoSmokingHistory

class ResponseSetPresenter:
    NOT_ANSWERED_TEXT = "Not answered"
    DATE_FORMAT = "%-d %B %Y" # eg 8 September 2000

    def __init__(self, response_set):
        self.response_set = response_set

    @property
    def have_you_ever_smoked(self):
        if not hasattr(self.response_set, 'have_you_ever_smoked_response'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.have_you_ever_smoked_response.get_value_display()

    @property
    def periods_when_you_stopped_smoking(self):
        if not hasattr(self.response_set, 'periods_when_you_stopped_smoking_response'):
            return self.NOT_ANSWERED_TEXT

        if self.response_set.periods_when_you_stopped_smoking_response.value:
            return f"Yes ({self.response_set.periods_when_you_stopped_smoking_response.duration_years} years)"
        else:
            return "No"

    @property
    def date_of_birth(self):
        if not hasattr(self.response_set, 'date_of_birth_response'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.date_of_birth_response.value.strftime(self.DATE_FORMAT)

    @property
    def height(self):
        if not hasattr(self.response_set, 'height_response'):
            return self.NOT_ANSWERED_TEXT

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
            return self.NOT_ANSWERED_TEXT

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
            return self.NOT_ANSWERED_TEXT

        return self.response_set.sex_at_birth_response.get_value_display()

    @property
    def gender(self):
        if not hasattr(self.response_set, 'gender_response'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.gender_response.get_value_display()

    @property
    def ethnicity(self):
        if not hasattr(self.response_set, 'ethnicity_response'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.ethnicity_response.get_value_display()

    @property
    def education(self):
        if not hasattr(self.response_set, 'education_response'):
            return self.NOT_ANSWERED_TEXT

        return self._list_to_sentence([
            EducationValues(code).label
            for code in self.response_set.education_response.value
        ])

    @property
    def asbestos_exposure(self):
        if not hasattr(self.response_set, 'asbestos_exposure_response'):
            return self.NOT_ANSWERED_TEXT

        return "Yes" if self.response_set.asbestos_exposure_response.value else "No"

    @property
    def cancer_diagnosis(self):
        if not hasattr(self.response_set, 'cancer_diagnosis_response'):
            return self.NOT_ANSWERED_TEXT

        return "Yes" if self.response_set.cancer_diagnosis_response.value else "No"

    @property
    def family_history_lung_cancer(self):
        if not hasattr(self.response_set, 'family_history_lung_cancer'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.family_history_lung_cancer.get_value_display()

    @property
    def relatives_age_when_diagnosed(self):
        if not hasattr(self.response_set, 'relatives_age_when_diagnosed'):
            return self.NOT_ANSWERED_TEXT

        return self.response_set.relatives_age_when_diagnosed.get_value_display()

    @property
    def age_when_started_smoking(self):
        if not hasattr(self.response_set, 'age_when_started_smoking_response'):
            return self.NOT_ANSWERED_TEXT

        return str(self.response_set.age_when_started_smoking_response.value)

    @property
    def respiratory_conditions(self):
        if not hasattr(self.response_set, 'respiratory_conditions_response'):
            return self.NOT_ANSWERED_TEXT

        if RespiratoryConditionValues.NONE in self.response_set.respiratory_conditions_response.value:
            values_sentence = self._list_to_sentence([
                label
                for label in RespiratoryConditionValues.labels
                if label != RespiratoryConditionValues.NONE.label
            ], final_separator = "or")

            return f"No, I have not been diagnosed with {values_sentence}"

        return self._list_to_sentence([
            RespiratoryConditionValues(code).label
            for code in self.response_set.respiratory_conditions_response.value
        ])


    @property
    def types_tobacco_smoking(self):
        normal_history = self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.NORMAL
        )
        if normal_history.count() < 1:
            return self.NOT_ANSWERED_TEXT

        return self._list_to_sentence([
            h.human_type() for h in normal_history.in_form_order()
        ])


    def eligibility_responses_items(self):
        items = [
            self._check_your_answer_item(
                "Have you ever smoked tobacco?",
                self.have_you_ever_smoked,
                "questions:have_you_ever_smoked",
            ),
            self._check_your_answer_item(
                "Date of birth",
                self.date_of_birth,
                "questions:date_of_birth",
            ),
        ]

        return items

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

    def smoking_history_types_responses_items(self):
        results = []
        normal_history = self.response_set.tobacco_smoking_history.filter(
            level=TobaccoSmokingHistory.Levels.NORMAL
        )
        for type_history in normal_history.in_form_order():
            results.extend(self.smoking_history_summary_items_for_type(type_history))

        return results

    def smoking_history_summary_items_for_type(self, type_history):
        type_label = type_history.human_type().lower()
        tobacco_type_kwargs = {"tobacco_type": dasherize(type_history.type).lower()}

        return [
            self._check_your_answer_item(
                f"Do you currently smoke {type_label}?",
                self._boolean_response_to_yes_no(type_history, "smoking_current_response"),
                "questions:smoking_current",
                kwargs=tobacco_type_kwargs
            ),
            self._check_your_answer_item(
                f"Total number of years you have smoked {type_label}",
                type_history.smoked_total_years_response.value if hasattr(type_history, 'smoked_total_years_response') else self.NOT_ANSWERED_TEXT,
                "questions:smoked_total_years",
                kwargs = tobacco_type_kwargs
            ),
            self._check_your_answer_item(
                f"Current {singularize(type_label)} smoking",
                self._smoking_type_to_text(type_history),
                "questions:smoking_frequency",
                kwargs=tobacco_type_kwargs
            ),
            self._check_your_answer_item(
                f"Has the number of {type_label} you normally smoke changed over time?",
                self._smoking_change_to_text(type_history),
                "questions:smoking_change",
                kwargs=tobacco_type_kwargs
            ),
        ]


    def _smoking_type_to_text(self, type_history):
        if not hasattr(type_history, 'smoking_frequency_response') or not hasattr(type_history, 'smoked_amount_response'):
            return self.NOT_ANSWERED_TEXT

        return f"{type_history.smoked_amount_response.value} {type_history.human_type().lower()} a {type_history.smoking_frequency_response.get_value_display_as_singleton_text()}"

    def _smoking_change_to_text(self, type_history):
        history_for_type = self.response_set.tobacco_smoking_history.filter(
            type=type_history.type
        )
        if history_for_type.filter(level=TobaccoSmokingHistory.Levels.INCREASED).exists():
            return "Yes, I used to smoke more"
        if history_for_type.filter(level=TobaccoSmokingHistory.Levels.DECREASED).exists():
            return "Yes, I used to smoke fewer"
        return "No, it has not changed"


    def smoking_history_responses_items(self):
        return [
            self._check_your_answer_item(
                "Age you started smoking",
                self.age_when_started_smoking,
                "questions:age_when_started_smoking",
            ),
            self._check_your_answer_item(
                "Have you ever stopped smoking for periods of 1 year or longer?",
                self.periods_when_you_stopped_smoking,
                "questions:periods_when_you_stopped_smoking",
            ),
            self._check_your_answer_item(
                "Types of tobacco smoked",
                self.types_tobacco_smoking,
                "questions:types_tobacco_smoking",
            ),
            *self.smoking_history_types_responses_items(),
        ]


    def is_complete(self):
        return self.response_set.is_complete()


    def _list_to_sentence(self, list, final_separator = "and"):
        if len(list) == 0:
            return ''
        if len(list) == 1:
            return list[0]
        if len(list) == 2:
            return f"{list[0]} {final_separator} {list[1]}"

        return f"{', '.join(list[:-1])}, {final_separator} {list[-1]}"


    def _should_display_relatives_age_when_diagnosed(self):
        return (
            hasattr(self.response_set, "family_history_lung_cancer")
            and self.response_set.family_history_lung_cancer.value == FamilyHistoryLungCancerValues.YES
        )


    def _change_query_params(self):
        return { "change": "True" }


    def _check_your_answer_item(self, question, value, url_lookup_name, kwargs = {}):
        return {
            "key": { "text": question },
            "value": { "text": value },
            "actions": {
                "items": [
                    {
                        "href": reverse(url_lookup_name, kwargs = kwargs, query = self._change_query_params()),
                        "text": "Change"
                    }
                ]
            }
        }

    def _boolean_response_to_yes_no(self, response, attribute_name, yes_text = "Yes", no_text = "No"):
        if hasattr(response, attribute_name):
            result = getattr(response, attribute_name).value
            if result is True:
                return yes_text
            elif result is False:
                return no_text
        else:
            return self.NOT_ANSWERED_TEXT
