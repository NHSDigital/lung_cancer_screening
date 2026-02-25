import factory

from .response_set_factory import ResponseSetFactory
from ...models.tobacco_smoking_history import (
    TobaccoSmokingHistory,
    TobaccoSmokingHistoryTypes,
)


class TobaccoSmokingHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TobaccoSmokingHistory

    response_set = factory.SubFactory(ResponseSetFactory)
    type = TobaccoSmokingHistoryTypes.CIGARETTES

    class Params:
        complete = factory.Trait(
            smoked_total_years_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.smoked_total_years_response_factory.SmokedTotalYearsResponseFactory",
                factory_related_name="tobacco_smoking_history"
            ),
            smoked_amount_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.smoked_amount_response_factory.SmokedAmountResponseFactory",
                factory_related_name="tobacco_smoking_history"
            ),
            smoking_frequency_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.smoking_frequency_response_factory.SmokingFrequencyResponseFactory",
                factory_related_name="tobacco_smoking_history"
            ),
            smoking_current_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.smoking_current_response_factory.SmokingCurrentResponseFactory",
                factory_related_name="tobacco_smoking_history"
            )
        )

        # Types
        cigarettes = factory.Trait(
            type=TobaccoSmokingHistoryTypes.CIGARETTES,
        )
        cigars = factory.Trait(
            type=TobaccoSmokingHistoryTypes.CIGARS,
        )
        rolled_cigarettes = factory.Trait(
            type=TobaccoSmokingHistoryTypes.ROLLED_CIGARETTES,
        )
        pipe = factory.Trait(
            type=TobaccoSmokingHistoryTypes.PIPE,
        )
        cigarillos = factory.Trait(
            type=TobaccoSmokingHistoryTypes.CIGARILLOS,
        )

        # Levels
        normal = factory.Trait(
            level=TobaccoSmokingHistory.Levels.NORMAL,
        )
        increased = factory.Trait(
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        decreased = factory.Trait(
            level=TobaccoSmokingHistory.Levels.DECREASED,
        )
