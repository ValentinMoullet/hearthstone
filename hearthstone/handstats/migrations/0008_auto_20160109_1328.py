# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0007_game_opponent_cards_nb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='opponent_cards_nb',
        ),
        migrations.AddField(
            model_name='game',
            name='opponent_hand_cards_nb',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='opponent_remaining_cards',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='realcard',
            name='prob_in_hand',
            field=models.FloatField(default=0.0),
        ),
    ]
