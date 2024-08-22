# Generated by Django 5.1 on 2024-08-21 05:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('capacidade', models.IntegerField()),
                ('quantidade_alunos', models.IntegerField(blank=True, null=True)),
                ('ra_professor', models.ForeignKey(limit_choices_to={'groups__name': 'Professor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
