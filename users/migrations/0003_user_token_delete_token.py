# Generated by Django 5.0 on 2024-05-13 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_token_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.IntegerField(default=4000),
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]