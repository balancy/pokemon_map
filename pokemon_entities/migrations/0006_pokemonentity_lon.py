# Generated by Django 3.1.7 on 2021-03-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_auto_20210326_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='lon',
            field=models.FloatField(default=1.0),
            preserve_default=False,
        ),
    ]