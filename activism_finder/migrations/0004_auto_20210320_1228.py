# Generated by Django 3.1.7 on 2021-03-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activism_finder', '0003_auto_20210320_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='code',
            field=models.CharField(max_length=24, unique=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]