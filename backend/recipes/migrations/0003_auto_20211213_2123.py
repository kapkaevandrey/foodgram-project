# Generated by Django 3.2.10 on 2021-12-13 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
    ]
