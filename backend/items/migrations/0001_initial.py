# Generated by Django 5.2 on 2025-05-01 11:09

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('locations', '0002_alter_building_name_alter_department_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('item_img_url', models.URLField(blank=True, null=True)),
                ('status', models.CharField(choices=[('lost', 'lost'), ('found', 'found'), ('claimed', 'claimed')], max_length=10)),
                ('owner_identified', models.BooleanField(default=False)),
                ('owner_name', models.CharField(blank=True, max_length=150, null=True)),
                ('owner_contact', models.CharField(blank=True, max_length=150, null=True)),
                ('date_reported_turned_in', models.DateField(auto_now_add=True)),
                ('date_claimed_returned', models.DateField(auto_now_add=True)),
                ('accepted_by_name', models.CharField(max_length=250)),
                ('turned_in_by_name', models.CharField(blank=True, max_length=150, null=True)),
                ('turned_in_by_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('claimed_by_id_verified', models.BooleanField(default=False)),
                ('claimed_by', models.CharField(max_length=150)),
                ('item_returned_by_name', models.CharField(max_length=250)),
                ('accepted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_items', to='accounts.profile')),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.building')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.department')),
                ('item_returned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='returned_items', to='accounts.profile')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.level')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.location')),
            ],
        ),
    ]
