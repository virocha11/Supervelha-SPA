# Generated by Django 5.1 on 2024-09-04 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionario', '0002_respondidopor_avaliado_alter_respondidopor_nota'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respondidopor',
            old_name='questioniaro',
            new_name='questionario',
        ),
    ]
