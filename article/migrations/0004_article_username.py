# Generated by Django 2.0.7 on 2018-08-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180726_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='username',
            field=models.CharField(default='admin', max_length=128),
            preserve_default=False,
        ),
    ]
