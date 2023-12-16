# Generated by Django 4.2.7 on 2023-12-12 19:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0011_gamecollection'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GameCollection',
            new_name='GameCollectionItem',
        ),
        migrations.AlterModelOptions(
            name='gamecollectionitem',
            options={'ordering': ['stage']},
        ),
        migrations.RenameField(
            model_name='gamecollectionitem',
            old_name='status',
            new_name='stage',
        ),
    ]
