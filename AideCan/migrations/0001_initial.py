# Generated by Django 2.2.1 on 2019-05-22 20:57

import datetime
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
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=250)),
                ('establishment', models.CharField(max_length=100)),
                ('photo', models.FileField(default='images/default.jpg', upload_to='images/', verbose_name='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mammography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mammography', models.FileField(null=True, upload_to='images/', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AideCan.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_tissue', models.CharField(choices=[('F', 'Fatty'), ('g', 'Fatty-glandular'), ('D', 'Dense-glandular')], max_length=16)),
                ('abnormality_present', models.CharField(choices=[('CALC', 'Calcification'), ('CIRC', 'Well - defined / circumscribed masses'), ('SPIC', 'Spiculated masses'), ('MISC', 'Other, ill - defined masses'), ('ARCH', 'Architectural distortion'), ('ASYM', 'Asymmetry'), ('NORM', 'Normal')], max_length=40)),
                ('Severity_of_abnormality', models.CharField(blank=True, choices=[('M', 'Malignant'), ('B', 'Benign')], max_length=10, null=True)),
                ('Cercle', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date', models.DateField(default=datetime.date(2019, 5, 22))),
                ('mammography', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AideCan.Mammography')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AideCan.Doctor')),
            ],
        ),
    ]