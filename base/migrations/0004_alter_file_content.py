# Generated by Django 4.2.5 on 2023-09-28 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_file_is_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
