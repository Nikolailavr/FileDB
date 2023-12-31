# Generated by Django 4.2.7 on 2023-11-20 04:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('type1', 'Type_1'), ('type2', 'Type_2')], db_index=True, max_length=10)),
                ('vendor', models.CharField(db_index=True, max_length=50)),
                ('date_revision', models.DateField(db_index=True)),
                ('extra_field', models.JSONField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['id'], name='filedb_file_id_a39e7c_idx'), models.Index(fields=['type'], name='filedb_file_type_979123_idx'), models.Index(fields=['vendor'], name='filedb_file_vendor_232076_idx'), models.Index(fields=['date_revision'], name='filedb_file_date_re_887b31_idx')],
            },
        ),
    ]
