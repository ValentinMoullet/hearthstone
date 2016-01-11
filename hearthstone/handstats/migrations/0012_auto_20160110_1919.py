# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0011_realcard_bias_coeff'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cards_used_by_opponent',
            field=models.ManyToManyField(to='handstats.RealCard'),
        ),
        migrations.AddField(
            model_name='realcard',
            name='prob_two_in_hand',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='realcard',
            name='nb_copy',
            field=models.IntegerField(default=0),
        ),
    ]
