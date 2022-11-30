# Generated by Django 4.1.2 on 2022-11-30 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promise_tracker', '0007_rating_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='promise',
            name='politician',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='promise_tracker.politician'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='promise',
            name='creator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
