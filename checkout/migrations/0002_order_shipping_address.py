# Generated by Django 5.1.6 on 2025-02-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
