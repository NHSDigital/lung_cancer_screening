# Generated manually to create GenderResponse and copy data

import django.db.models.deletion
from django.db import migrations, models


def copy_gender_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_genderresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), gender, id
            FROM questions_responseset
            WHERE gender IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_gender_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET gender = g.value
            FROM questions_genderresponse g
            WHERE rs.id = g.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0028_ethnicityresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenderResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('N', 'Non-binary'), ('P', 'Prefer not to say'), ('G', 'How I describe myself may not match my GP record')], max_length=1)),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gender_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_gender_data, reverse_copy_gender_data),
        migrations.RemoveField(
            model_name='responseset',
            name='gender',
        ),
    ]
