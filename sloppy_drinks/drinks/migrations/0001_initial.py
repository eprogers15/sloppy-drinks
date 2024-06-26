# Generated by Django 4.2.11 on 2024-03-20 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('slug', models.SlugField(default='')),
                ('recipe_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSource',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(help_text='Enter an ingredient name (e.g. Simple Syrup)', max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeSource',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('filename', models.CharField(max_length=240, primary_key=True, serialize=False)),
                ('recipe', models.BooleanField(default=False)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drinks.drink')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drinks.imagesource')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('date', models.DateField(unique=True)),
                ('acast_url', models.URLField(default='https://play.acast.com/s/thesloppyboys/')),
                ('spotify_url', models.URLField(default='https://open.spotify.com/show/3qFjDCQ16YrjFw5ufNpV3c?si=4202cac534494845')),
                ('instagram_post_url', models.URLField(blank=True, null=True)),
                ('twitter_post_url', models.URLField(blank=True, null=True)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drinks.drink')),
            ],
        ),
        migrations.AddField(
            model_name='drink',
            name='ingredients',
            field=models.ManyToManyField(help_text='Select the ingredients for this drink', to='drinks.ingredient'),
        ),
        migrations.AddField(
            model_name='drink',
            name='recipe_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='drinks.recipesource'),
        ),
    ]
