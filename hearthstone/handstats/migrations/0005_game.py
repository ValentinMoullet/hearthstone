# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0004_auto_20160107_0446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opponent_hero', models.CharField(max_length=200)),
                ('first_to_play', models.BooleanField()),
                ('decks', models.ManyToManyField(to='handstats.Deck')),
            ],
        ),
    ]
