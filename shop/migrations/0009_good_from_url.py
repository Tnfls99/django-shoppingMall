# Generated by Django 3.2.7 on 2021-12-05 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20211203_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='from_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
