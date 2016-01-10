# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handstats', '0008_auto_20160109_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckInGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cards', models.ManyToManyField(to='handstats.RealCard')),
                ('deck', models.ForeignKey(to='handstats.Deck')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='update_opponent_prob_maybe_todo_list',
            field=models.ManyToManyField(related_name='update_opponent_prob_maybe_todo_list', to='handstats.Card'),
        ),
        migrations.AddField(
            model_name='game',
            name='update_opponent_prob_sure_todo_list',
            field=models.ManyToManyField(related_name='update_opponent_prob_sure_todo_list', to='handstats.Card'),
        ),
        migrations.AddField(
            model_name='game',
            name='use_opponent_card_todo_list',
            field=models.ManyToManyField(related_name='use_opponent_card_todo_list', to='handstats.Card'),
        ),
        migrations.AlterField(
            model_name='game',
            name='decks',
            field=models.ManyToManyField(to='handstats.DeckInGame'),
        ),
    ]
