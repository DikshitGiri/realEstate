# Generated by Django 4.2.3 on 2023-11-07 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('price_range', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='property_images/')),
                ('details', models.TextField()),
                ('status', models.TextField(default='Available')),
                ('sold_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('price_range', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.TextField()),
                ('image', models.ImageField(upload_to='notification_images/')),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('inquires', models.TextField(default='not inquired')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
