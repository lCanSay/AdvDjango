# Generated by Django 5.2 on 2025-04-02 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_expense_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
