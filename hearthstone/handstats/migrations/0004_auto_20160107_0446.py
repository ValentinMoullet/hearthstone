# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0003_deckcreation_nb_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(to='handstats.RealCard'),
        ),
    ]
