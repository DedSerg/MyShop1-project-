# Generated by Django 4.2.16 on 2024-12-17 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myshop_dj', '0018_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='myshop_dj.cart'),
        ),
    ]
