# Generated by Django 4.1.7 on 2023-08-28 18:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_item_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]