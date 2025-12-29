# Generated manually to create DateOfBirthResponse and copy data

import django.db.models.deletion
from django.db import migrations, models


def copy_date_of_birth_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_dateofbirthresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), date_of_birth, id
            FROM questions_responseset
            WHERE date_of_birth IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_date_of_birth_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET date_of_birth = d.value
            FROM questions_dateofbirthresponse d
            WHERE rs.id = d.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0026_asbestosexposureresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateOfBirthResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.DateField()),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='date_of_birth_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_date_of_birth_data, reverse_copy_date_of_birth_data),
        migrations.RemoveField(
            model_name='responseset',
            name='date_of_birth',
        ),
    ]
