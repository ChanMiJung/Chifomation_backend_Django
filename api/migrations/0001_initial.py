# Generated by Django 3.2.12 on 2022-04-03 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('img_url', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('color', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chicken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('cost', models.IntegerField()),
                ('img_url', models.TextField(blank=True)),
                ('original_category', models.TextField()),
                ('introduction', models.TextField(blank=True)),
                ('hash_tag', models.TextField(blank=True)),
                ('new', models.BooleanField(default=False)),
                ('popularity', models.BooleanField(default=False)),
                ('score', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('star', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('chicken', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chicken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
