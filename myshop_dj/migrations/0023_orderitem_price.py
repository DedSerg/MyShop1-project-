# Generated by Django 4.2.16 on 2024-12-17 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop_dj', '0022_alter_orderitem_quantity_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
