from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0043_agewhenstartedsmokingresponse"),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodsWhenYouStoppedSmokingResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.BooleanField()),
                ('response_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='periods_when_you_stopped_smoking_response', to='questions.responseset')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
