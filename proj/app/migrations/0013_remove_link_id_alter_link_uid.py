# Generated by Django 4.0.3 on 2023-04-07 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='id',
        ),
        migrations.AlterField(
            model_name='link',
            name='uid',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]