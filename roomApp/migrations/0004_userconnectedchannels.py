# Generated by Django 4.1.2 on 2022-11-25 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roomApp', '0003_useronline'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConnectedChannels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_value', models.CharField(help_text='Every channel name consists of a specific 74 chars', max_length=74, verbose_name='Channel Name')),
                ('user_online', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserConnectionChannels', to='roomApp.useronline')),
            ],
        ),
    ]
