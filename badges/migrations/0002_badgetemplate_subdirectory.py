# Generated by Django 3.2.9 on 2021-11-02 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badgetemplate',
            name='subdirectory',
            field=models.CharField(default='', max_length=50),
        ),
    ]
