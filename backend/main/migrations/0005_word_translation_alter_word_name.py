# Generated by Django 5.0.1 on 2025-02-13 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userquestions_userwordcategories_userwords'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='translation',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
