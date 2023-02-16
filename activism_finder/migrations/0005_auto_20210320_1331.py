# Generated by Django 3.1.7 on 2021-03-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activism_finder', '0004_auto_20210320_1228'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='source',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, code='search'), name='no_search_code'),
        ),
        migrations.AddConstraint(
            model_name='source',
            constraint=models.CheckConstraint(check=models.Q(models.Q(_negated=True, code__contains=' '), models.Q(_negated=True, code__contains='/')), name='no_invalid_characters_code'),
        ),
    ]