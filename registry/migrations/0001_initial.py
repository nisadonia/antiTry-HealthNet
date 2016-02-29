# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 05:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.enum
import localflavor.us.models
import registry.utility.models
import registry.utility.options
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.TextField()),
                ('admitted_by', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.TextField()),
                ('contact_primary', localflavor.us.models.PhoneNumberField(max_length=20)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('providers', registry.utility.models.SeparatedValuesField()),
                ('side_effects', registry.utility.models.SeparatedValuesField()),
                ('msdsLink', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=300)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('identifiers', models.ForeignKey(default=registry.utility.models.Dictionary.empty, on_delete=models.SET(registry.utility.models.Dictionary.empty), to='registry.Dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('key', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('value', models.TextField()),
                ('dict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.TextField()),
                ('doctor', models.TextField()),
                ('sign_off', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('content', models.TextField()),
                ('images', registry.utility.models.SeparatedValuesField()),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('refills', models.PositiveIntegerField()),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='registry.Drug')),
            ],
        ),
        migrations.CreateModel(
            name='TimeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('middle_initial', models.CharField(blank=True, default='', max_length=1)),
                ('date_of_birth', models.DateField()),
                ('gender', models.IntegerField(choices=[(0, django_enumfield.enum.Value('MALE', 0, 'M', registry.utility.options.Gender)), (1, django_enumfield.enum.Value('FEMALE', 1, 'F', registry.utility.options.Gender))], default=0, max_length=1)),
                ('security_question', models.IntegerField(choices=[(0, django_enumfield.enum.Value('Q1', 0, "What is your mother's maiden name?", registry.utility.options.SecurityQuestion))], default=0, max_length=100)),
                ('security_answer', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.User')),
                ('is_sysadmin', models.BooleanField(default=False)),
            ],
            bases=('registry.user',),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.User')),
                ('hospitals', models.ManyToManyField(related_name='provider_to', to='registry.Hospital')),
            ],
            bases=('registry.user',),
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('medicaldata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.MedicalData')),
            ],
            bases=('registry.medicaldata',),
        ),
        migrations.CreateModel(
            name='MedicalTest',
            fields=[
                ('medicaldata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.MedicalData')),
                ('timestamp', models.DateTimeField()),
                ('images', registry.utility.models.SeparatedValuesField()),
                ('results', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_note', to='registry.Note')),
                ('sign_off_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registry.Doctor')),
            ],
            bases=('registry.medicaldata',),
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.User')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Hospital')),
            ],
            bases=('registry.user',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.User')),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('blood_type', models.IntegerField(choices=[(0, django_enumfield.enum.Value('A', 0, 'A', registry.utility.options.BloodType)), (1, django_enumfield.enum.Value('B', 1, 'B', registry.utility.options.BloodType)), (2, django_enumfield.enum.Value('AB', 2, 'AB', registry.utility.options.BloodType)), (3, django_enumfield.enum.Value('O', 3, 'O', registry.utility.options.BloodType)), (4, django_enumfield.enum.Value('UNKNOWN', 4, '--', registry.utility.options.BloodType))], default=4, max_length=2)),
                ('insurance', models.CharField(choices=[('Self Insured', 'Self Insured'), ('Blue Cross Blue Shield', 'Blue Cross Blue Shield'), ('Super Legit MI', 'Super Legit Medical Insurance'), ('Not Legit MI', 'Not Legit Medical Insurance')], default='Self Insured', max_length=40)),
            ],
            bases=('registry.user',),
        ),
        migrations.CreateModel(
            name='PatientContact',
            fields=[
                ('contact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registry.Contact')),
                ('relationship', models.IntegerField(choices=[(0, django_enumfield.enum.Value('SPOUSE', 0, 'SPOUSE', registry.utility.options.Relationship)), (1, django_enumfield.enum.Value('MOTHER', 1, 'MOTHER', registry.utility.options.Relationship)), (2, django_enumfield.enum.Value('FATHER', 2, 'FATHER', registry.utility.options.Relationship)), (3, django_enumfield.enum.Value('BROTHER', 3, 'BROTHER', registry.utility.options.Relationship)), (4, django_enumfield.enum.Value('SISTER', 4, 'SISTER', registry.utility.options.Relationship)), (5, django_enumfield.enum.Value('FAMILY', 5, 'FAMILY', registry.utility.options.Relationship)), (6, django_enumfield.enum.Value('FRIEND', 6, 'FRIEND', registry.utility.options.Relationship)), (7, django_enumfield.enum.Value('OTHER', 7, 'OTHER', registry.utility.options.Relationship))], default=7, max_length=20)),
                ('contact_seconday', localflavor.us.models.PhoneNumberField(max_length=20)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Patient')),
            ],
            bases=('registry.contact',),
        ),
        migrations.AddField(
            model_name='user',
            name='auth_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='cur_hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registry_user_cur_hospital', to='registry.Hospital'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='time_range',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='registry.TimeRange'),
        ),
        migrations.AddField(
            model_name='medicaldata',
            name='notes',
            field=models.ManyToManyField(related_name='registry_medicaldata_medical_notes', to='registry.Note'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Hospital'),
        ),
        migrations.AddField(
            model_name='admissioninfo',
            name='admission_time',
            field=models.OneToOneField(default=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='registry.TimeRange'),
        ),
        migrations.AddField(
            model_name='admissioninfo',
            name='prescriptions',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='registry.Dictionary'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Doctor'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registry.Patient'),
        ),
        migrations.AddField(
            model_name='patient',
            name='admission_status',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_status', to='registry.AdmissionInfo'),
        ),
        migrations.AddField(
            model_name='patient',
            name='pref_hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registry_patient_pref_hospital', to='registry.Hospital'),
        ),
        migrations.AddField(
            model_name='patient',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='providers', to='registry.Doctor'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='admission_details',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registry.AdmissionInfo'),
        ),
        migrations.AddField(
            model_name='medicaldata',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_info', to='registry.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='nurse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registry.Nurse'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Patient'),
        ),
        migrations.AddField(
            model_name='admissioninfo',
            name='doctors',
            field=models.ManyToManyField(to='registry.Doctor'),
        ),
    ]
