# Generated by Django 4.2.2 on 2023-10-09 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_file_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='temp_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]