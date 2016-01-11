# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0009_auto_20160109_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckAbstraction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cards', models.ManyToManyField(to='handstats.RealCard')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='opponent_deck_abstraction',
            field=models.ForeignKey(default=0, to='handstats.DeckAbstraction'),
            preserve_default=False,
        ),
    ]
