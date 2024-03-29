# Generated by Django 4.1.2 on 2022-10-20 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promise_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyvalidity',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parties_validity', to='promise_tracker.party'),
        ),
        migrations.AlterField(
            model_name='partyvalidity',
            name='politician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parties_validity', to='promise_tracker.politician'),
        ),
    ]
