# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0010_auto_20160110_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='realcard',
            name='bias_coeff',
            field=models.FloatField(default=1.0),
        ),
    ]
