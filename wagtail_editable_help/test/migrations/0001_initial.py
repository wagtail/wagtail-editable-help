# Generated by Django 3.2.15 on 2022-09-08 12:28

from django.db import migrations, models
import django.db.models.deletion
import wagtail_editable_help.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('tagline', models.CharField(help_text=wagtail_editable_help.models.HelpText('Home page', 'tagline', default='Write something snappy here'), max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
