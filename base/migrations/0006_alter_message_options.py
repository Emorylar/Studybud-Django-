# Generated by Django 5.1.1 on 2024-10-19 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
