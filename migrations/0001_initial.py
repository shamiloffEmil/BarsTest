# Generated by Django 2.2.5 on 2019-12-22 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=350)),
            ],
            options={
                'ordering': ('question',),
            },
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('planetOfResidence', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BarsTest.Planet')),
            ],
        ),
        migrations.CreateModel(
            name='TestHandShadow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderСode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BarsTest.Order')),
                ('question', models.ManyToManyField(to='BarsTest.Question')),
            ],
            options={
                'ordering': ('orderСode',),
            },
        ),
        migrations.CreateModel(
            name='Sith',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('workPlanet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BarsTest.Planet')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ManyToManyField(to='BarsTest.Answer')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BarsTest.Recruit')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BarsTest.TestHandShadow')),
            ],
        ),
    ]
