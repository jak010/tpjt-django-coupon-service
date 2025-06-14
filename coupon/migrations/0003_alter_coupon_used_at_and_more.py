# Generated by Django 5.2.1 on 2025-06-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_alter_couponpolicy_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='used_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='couponpolicy',
            name='discount_type',
            field=models.CharField(choices=[('FIXED_AMOUNT', 'FIXED_AMOUNT'), ('PERCENT_AMOUNT', 'PERCENT_AMOUNT')], max_length=24),
        ),
        migrations.AlterField(
            model_name='couponpolicy',
            name='discount_value',
            field=models.PositiveIntegerField(),
        ),
    ]
