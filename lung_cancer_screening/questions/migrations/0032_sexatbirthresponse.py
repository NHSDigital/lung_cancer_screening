# Generated manually to create SexAtBirthResponse and copy data

import django.db.models.deletion
from django.db import migrations, models


def copy_sex_at_birth_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_sexatbirthresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), sex_at_birth, id
            FROM questions_responseset
            WHERE sex_at_birth IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_sex_at_birth_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET sex_at_birth = s.value
            FROM questions_sexatbirthresponse s
            WHERE rs.id = s.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0031_respiratoryconditionsresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='SexAtBirthResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1)),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sex_at_birth_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_sex_at_birth_data, reverse_copy_sex_at_birth_data),
        migrations.RemoveField(
            model_name='responseset',
            name='sex_at_birth',
        ),
    ]
