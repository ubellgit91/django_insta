# Generated by Django 2.1.3 on 2018-12-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_auto_20181203_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='filtered_image',
            field=models.ImageField(upload_to='%Y/%m/%d/filtered'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='%Y/%m/%d/origin'),
        ),
    ]