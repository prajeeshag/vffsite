# Generated by Django 3.0.8 on 2020-07-27 18:09

import accounts.managers
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be ten digits', regex='^(\\d{10})$')], verbose_name='phone number')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=True, verbose_name='staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TOTPDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='67fe6eeeafc41a6cd1aa5224bcf0f102cf9f9041', max_length=20)),
                ('step', models.PositiveSmallIntegerField(default=120)),
                ('last_t', models.BigIntegerField(default=-1)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('address_1', models.CharField(blank=True, max_length=250, verbose_name='Address line 1')),
                ('address_2', models.CharField(blank=True, max_length=250, verbose_name='Address line 2')),
                ('post_office', models.CharField(blank=True, max_length=50, verbose_name='Post Office')),
                ('district', models.CharField(blank=True, max_length=50, verbose_name='District/City')),
                ('state', models.CharField(blank=True, max_length=50, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Country')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Email address')),
                ('email_validated', models.BooleanField(default=True, editable=False)),
                ('jersey_size', models.CharField(blank=True, choices=[('XS', 'Extra small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra large'), ('2XL', 'Double extra large'), ('3XL', 'Triple extra large')], default='M', max_length=3, verbose_name='Jersey Size')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
