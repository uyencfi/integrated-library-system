# Generated by Django 3.1.7 on 2021-03-25 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_user_id', models.CharField(db_column='adminUserID', max_length=45, primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='passWord', max_length=15)),
            ],
            options={
                'db_table': 'Admins',
            },
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('user_id', models.OneToOneField(db_column='userID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='fines', serialize=False, to='auth.user')),
                ('amount', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Fines',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_id', models.CharField(db_column='userID', max_length=45, primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='passWord', max_length=15)),
            ],
            options={
                'db_table': 'Members',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_time', models.DateTimeField(db_column='transactionTime')),
                ('amount', models.FloatField(blank=True, db_column='paid', null=True)),
                ('card', models.CharField(blank=True, max_length=20, null=True)),
                ('user_id', models.ForeignKey(db_column='userID', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Payments',
                'ordering': ['-transaction_time'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.IntegerField(db_column='bookID', primary_key=True, serialize=False)),
                ('start_date', models.DateField(blank=True, db_column='startDate', null=True)),
                ('due_date', models.DateField(blank=True, db_column='dueDate', null=True)),
                ('reserve_due_date', models.DateField(blank=True, db_column='reserveDueDate', null=True)),
                ('return_date', models.DateField(blank=True, db_column='returnDate', null=True)),
                ('borrower_id', models.ForeignKey(blank=True, db_column='borrowerID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loans', to=settings.AUTH_USER_MODEL)),
                ('reserver_id', models.ForeignKey(blank=True, db_column='reserverID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Books',
                'ordering': ['book_id'],
            },
        ),
    ]