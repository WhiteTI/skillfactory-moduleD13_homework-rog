# Generated by Django 4.2.4 on 2023-09-02 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_ad_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
