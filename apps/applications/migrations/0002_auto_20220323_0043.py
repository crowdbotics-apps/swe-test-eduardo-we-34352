# Generated by Django 2.2.26 on 2022-03-23 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='created_by',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='app',
            name='framework',
            field=models.CharField(choices=[('D', 'Django'), ('R', 'React Native')], max_length=1),
        ),
        migrations.AlterField(
            model_name='app',
            name='type',
            field=models.CharField(choices=[('W', 'Web'), ('M', 'Mobile')], max_length=1),
        ),
    ]
