# Generated by Django 4.2.4 on 2023-08-25 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_posts_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
