# Generated manually to create EthnicityResponse and copy data

import django.db.models.deletion
from django.db import migrations, models


def copy_ethnicity_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions_ethnicityresponse (created_at, updated_at, value, response_set_id)
            SELECT NOW(), NOW(), ethnicity, id
            FROM questions_responseset
            WHERE ethnicity IS NOT NULL
            ON CONFLICT (response_set_id) DO NOTHING
        """)


def reverse_copy_ethnicity_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE questions_responseset rs
            SET ethnicity = e.value
            FROM questions_ethnicityresponse e
            WHERE rs.id = e.response_set_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0027_dateofbirthresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='EthnicityResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(choices=[('A', 'Asian or Asian British'), ('B', 'Black, African, Caribbean or Black British'), ('M', 'Mixed or multiple ethnic groups'), ('W', 'White'), ('O', 'Other ethnic group'), ('N', "I'd prefer not to say")], max_length=1)),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ethnicity_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(copy_ethnicity_data, reverse_copy_ethnicity_data),
        migrations.RemoveField(
            model_name='responseset',
            name='ethnicity',
        ),
    ]
