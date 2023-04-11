# Generated by Django 4.0.3 on 2023-04-10 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_delete_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('uid', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254)),
                ('password', models.CharField(default='<django.db.models.fields.CharField>', max_length=255)),
                ('dep', models.CharField(max_length=100)),
                ('mobile_num', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
            ],
        ),
    ]
