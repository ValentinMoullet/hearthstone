# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0006_game_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='opponent_cards_nb',
            field=models.IntegerField(default=5),
        ),
    ]
