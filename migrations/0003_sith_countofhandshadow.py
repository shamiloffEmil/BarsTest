# Generated by Django 2.2.5 on 2020-01-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarsTest', '0002_recruit_rankofhandshadow'),
    ]

    operations = [
        migrations.AddField(
            model_name='sith',
            name='CountOfHandShadow',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]