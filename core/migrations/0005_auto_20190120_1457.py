# Generated by Django 2.1.5 on 2019-01-20 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0004_auto_20180204_1439")]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"default_permissions": ("view", "add", "change", "delete")},
        )
    ]
