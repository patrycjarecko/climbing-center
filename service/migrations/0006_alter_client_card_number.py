# Generated by Django 3.2.9 on 2021-12-16 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_client_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='card_number',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]
