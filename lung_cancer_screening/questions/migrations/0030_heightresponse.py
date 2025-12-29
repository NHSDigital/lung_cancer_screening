# Generated manually to create HeightResponse and copy data

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def copy_height_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_heightresponse (created_at, updated_at, metric, imperial, response_set_id)
            SELECT NOW(), NOW(), height_metric, height_imperial, id
            FROM questions_responseset
            WHERE height_metric IS NOT NULL OR height_imperial IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_height_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET height_metric = h.metric,
                height_imperial = h.imperial
            FROM questions_heightresponse h
            WHERE rs.id = h.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0029_genderresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeightResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('metric', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1397, message='Height must be between 139.7cm and 243.8 cm'), django.core.validators.MaxValueValidator(2438, message='Height must be between 139.7cm and 243.8 cm')])),
                ('imperial', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(55, message='Height must be between 4 feet 7 inches and 8 feet'), django.core.validators.MaxValueValidator(96, message='Height must be between 4 feet 7 inches and 8 feet')])),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='height_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_height_data, reverse_copy_height_data),
        migrations.RemoveField(
            model_name='responseset',
            name='height_metric',
        ),
        migrations.RemoveField(
            model_name='responseset',
            name='height_imperial',
        ),
    ]
