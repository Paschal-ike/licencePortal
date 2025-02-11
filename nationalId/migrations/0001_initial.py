# Generated by Django 4.2.4 on 2024-07-12 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NationalId',
            fields=[
                ('idNo', models.IntegerField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=255)),
                ('middleName', models.CharField(blank=True, max_length=255, null=True)),
                ('lastName', models.CharField(blank=True, max_length=255, null=True)),
                ('DOB', models.DateField()),
                ('Sex', models.CharField(blank=True, max_length=10, null=True)),
                ('Passport', models.ImageField(blank=True, null=True, upload_to='passports/')),
                ('issuedAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
