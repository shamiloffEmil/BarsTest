# Generated by Django 2.2.5 on 2020-03-01 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BarsTest', '0003_sith_countofhandshadow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sith',
            old_name='CountOfHandShadow',
            new_name='countOfHandShadow',
        ),
    ]
