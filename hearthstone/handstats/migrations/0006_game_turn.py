# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0005_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.IntegerField(default=1),
        ),
    ]
