# Generated by Django 3.2.10 on 2021-12-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20211210_1335'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('type', 'quantity'), name='unique ingredient'),
        ),
    ]
