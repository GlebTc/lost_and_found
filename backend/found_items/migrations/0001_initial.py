# Generated by Django 5.0.3 on 2024-03-07 19:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoundItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField(blank=True, null=True)),
                ('log_item_number', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('found_location', models.CharField(blank=True, max_length=100, null=True)),
                ('item_description', models.TextField()),
                ('received_by', models.CharField(max_length=100)),
                ('turned_in_by', models.CharField(blank=True, max_length=100, null=True)),
                ('claimed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('released_by', models.CharField(blank=True, max_length=100, null=True)),
                ('date_released', models.DateField(blank=True, null=True)),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
    ]