# Generated by Django 2.2.26 on 2022-03-23 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO applications_plan (name, price, description, created_at, updated_at) VALUES
            ('Free', 0, 'Free plan', now(), now()),
            ('Standard', 10, 'Standard plan', now(), now()),
            ('Pro', 25, 'Pro plan', now(), now());
            """
        )
    ]
