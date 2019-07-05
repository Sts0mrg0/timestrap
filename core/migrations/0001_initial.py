import conf.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("archive", models.BooleanField(default=False)),
                ("payment_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "invoice_email",
                    models.EmailField(blank=True, max_length=255, null=True),
                ),
                ("sites", models.ManyToManyField(to="sites.Site")),
            ],
            options={
                "default_permissions": ("view", "add", "change", "delete"),
                "ordering": ["-id"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", conf.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(blank=True)),
                ("duration", models.DurationField(blank=True)),
                ("note", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Entries",
                "ordering": ["-date", "-id"],
                "default_permissions": ("view", "add", "change", "delete"),
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", conf.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("paid", models.DateTimeField(blank=True, null=True)),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Client"
                    ),
                ),
                (
                    "entries",
                    models.ManyToManyField(related_name="invoices", to="core.Entry"),
                ),
                (
                    "site",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sites.Site",
                    ),
                ),
            ],
            options={"default_permissions": ("view", "add", "change", "delete")},
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", conf.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("archive", models.BooleanField(default=False)),
                (
                    "estimate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="core.Client",
                    ),
                ),
            ],
            options={
                "default_permissions": ("view", "add", "change", "delete"),
                "ordering": ["client", "-id"],
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "hourly_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("sites", models.ManyToManyField(to="sites.Site")),
            ],
            options={
                "default_permissions": ("view", "add", "change", "delete"),
                "ordering": ["-id"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", conf.managers.CurrentSiteManager()),
            ],
        ),
        migrations.AddField(
            model_name="entry",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to="core.Project",
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="site",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="sites.Site"
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to="core.Task",
            ),
        ),
        migrations.AddField(
            model_name="entry",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
