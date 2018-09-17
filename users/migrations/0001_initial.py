# Generated by Django 2.1.1 on 2018-09-17 02:28

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('other_names', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=25, null=True, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-date_joined', 'first_name'),
            },
        ),
    ]
