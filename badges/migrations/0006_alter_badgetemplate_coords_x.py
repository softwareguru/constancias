# Generated by Django 3.2.9 on 2022-06-24 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0005_auto_20220624_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgetemplate',
            name='coords_x',
            field=models.IntegerField(blank=True, default=107, null=True),
        ),
    ]
