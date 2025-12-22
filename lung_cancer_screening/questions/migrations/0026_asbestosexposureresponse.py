# Generated manually to create AsbestosExposureResponse and copy data

import django.db.models.deletion
from django.db import migrations, models


def copy_asbestos_exposure_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_asbestosexposureresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), asbestos_exposure, id
            FROM questions_responseset
            WHERE asbestos_exposure IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_asbestos_exposure_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET asbestos_exposure = a.value
            FROM questions_asbestosexposureresponse a
            WHERE rs.id = a.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0025_haveyoueversmokedresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsbestosExposureResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.BooleanField()),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='asbestos_exposure_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_asbestos_exposure_data, reverse_copy_asbestos_exposure_data),
        migrations.RemoveField(
            model_name='responseset',
            name='asbestos_exposure',
        ),
    ]
