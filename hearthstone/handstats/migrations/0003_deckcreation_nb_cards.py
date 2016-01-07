# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0002_auto_20160106_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckcreation',
            name='nb_cards',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
