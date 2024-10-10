import os

from django.contrib.auth.models import User
from django.db import migrations


def create_superuser(apps, schema_editor):
    username = os.environ.get("SUPERUSER_USERNAME")
    email = os.environ.get("SUPERUSER_EMAIL")
    password = os.environ.get("SUPERUSER_PASSWORD")

    if username and email and password:
        if User.objects.filter(username=username).first() is None:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser, migrations.RunPython.noop),
    ]
