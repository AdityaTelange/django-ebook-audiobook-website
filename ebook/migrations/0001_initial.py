# Generated by Django 2.2.5 on 2019-09-10 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('welut', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('slug', models.SlugField(max_length=48)),
                ('active', models.BooleanField(default=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('ebook_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebook_file', to='welut.EbookConverter')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='EbookTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('slug', models.SlugField(max_length=48)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EbookImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product-images')),
                ('thumbnail', models.ImageField(null=True, upload_to='product-thumbnails')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook.Ebook')),
            ],
        ),
        migrations.AddField(
            model_name='ebook',
            name='tags',
            field=models.ManyToManyField(blank=True, to='ebook.EbookTag'),
        ),
    ]
