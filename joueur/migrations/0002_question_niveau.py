# Generated by Django 4.2.5 on 2023-10-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joueur', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='niveau',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
