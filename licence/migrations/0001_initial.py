# Generated by Django 4.2.4 on 2024-07-12 22:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nationalId', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licenseId', models.CharField(max_length=20, unique=True)),
                ('issue_date', models.DateField(default=django.utils.timezone.now)),
                ('expiry_date', models.DateField()),
                ('passport_photo', models.ImageField(upload_to='passport_photos/')),
                ('IdNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nationalId.nationalid')),
            ],
        ),
    ]
