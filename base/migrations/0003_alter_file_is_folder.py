# Generated by Django 4.2.5 on 2023-09-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_file_body_file_content_file_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='is_folder',
            field=models.BooleanField(default=False),
        ),
    ]