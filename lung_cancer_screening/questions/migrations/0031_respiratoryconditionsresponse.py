# Generated manually to create RespiratoryConditionsResponse and copy data

import django.contrib.postgres.fields
import django.db.models.deletion
import lung_cancer_screening.questions.models.respiratory_conditions_response
from django.db import migrations, models


def copy_respiratory_conditions_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_respiratoryconditionsresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), respiratory_conditions, id
            FROM questions_responseset
            WHERE respiratory_conditions IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_respiratory_conditions_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET respiratory_conditions = r.value
            FROM questions_respiratoryconditionsresponse r
            WHERE rs.id = r.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0030_heightresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='RespiratoryConditionsResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('P', 'Pneumonia'), ('E', 'Emphysema'), ('B', 'Bronchitis'), ('T', 'Tuberculosis (TB)'), ('C', 'Chronic obstructive pulmonary disease (COPD)'), ('N', 'No, I have not had any of these respiratory conditions')], max_length=1), size=None, validators=[lung_cancer_screening.questions.models.validators.singleton_option.validate_singleton_option])),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='respiratory_conditions_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_respiratory_conditions_data, reverse_copy_respiratory_conditions_data),
        migrations.RemoveField(
            model_name='responseset',
            name='respiratory_conditions',
        ),
    ]
