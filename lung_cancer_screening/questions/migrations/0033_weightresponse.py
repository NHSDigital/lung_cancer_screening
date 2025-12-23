# Generated manually to create WeightResponse and copy data

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def copy_weight_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_weightresponse (created_at, updated_at, metric, imperial, response_set_id)
            SELECT NOW(), NOW(), weight_metric, weight_imperial, id
            FROM questions_responseset
            WHERE weight_metric IS NOT NULL OR weight_imperial IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_weight_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET weight_metric = w.metric,
                weight_imperial = w.imperial
            FROM questions_weightresponse w
            WHERE rs.id = w.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0032_sexatbirthresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('metric', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(254, message='Weight must be between 25.4kg and 317.5kg'), django.core.validators.MaxValueValidator(3175, message='Weight must be between 25.4kg and 317.5kg')])),
                ('imperial', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(56, message='Weight must be between 4 stone and 50 stone'), django.core.validators.MaxValueValidator(700, message='Weight must be between 4 stone and 50 stone')])),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='weight_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_weight_data, reverse_copy_weight_data),
        migrations.RemoveField(
            model_name='responseset',
            name='weight_metric',
        ),
        migrations.RemoveField(
            model_name='responseset',
            name='weight_imperial',
        ),
    ]
