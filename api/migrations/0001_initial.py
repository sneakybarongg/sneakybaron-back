# Generated by Django 2.2.2 on 2019-06-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summoner_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('main_champion', models.CharField(max_length=255)),
            ],
        ),
    ]
