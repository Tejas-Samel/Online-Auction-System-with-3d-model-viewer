# Generated by Django 3.2.7 on 2021-10-08 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20211007_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='imageUrl',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(default=0, max_length=20)),
                ('phone', models.CharField(default=0, max_length=15)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
