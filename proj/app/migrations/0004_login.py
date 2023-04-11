# Generated by Django 4.0.3 on 2023-03-23 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_delete_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('uid', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('student', models.BooleanField(default=False)),
                ('teacher', models.BooleanField(default=False)),
                ('parent', models.BooleanField(default=False)),
            ],
        ),
    ]
