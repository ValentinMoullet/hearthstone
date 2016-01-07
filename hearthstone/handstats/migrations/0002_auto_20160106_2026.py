# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckCreation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hero', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RealCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nb_copy', models.IntegerField()),
                ('card', models.ForeignKey(to='handstats.Card')),
            ],
        ),
        migrations.AddField(
            model_name='deckcreation',
            name='real_cards',
            field=models.ManyToManyField(to='handstats.RealCard'),
        ),
    ]
