# Generated by Django 3.0.2 on 2020-02-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlcmp', '0002_auto_20200116_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlcmp',
            name='platform_name',
        ),
        migrations.AddField(
            model_name='mlcmp',
            name='result',
            field=models.TextField(default=' ', max_length=555),
            preserve_default=False,
        ),
    ]
