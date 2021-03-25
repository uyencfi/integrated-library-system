# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# from django_mongoengine import Document, EmbeddedDocument
# from django_mongoengine import fields
# class User overridden? -> settings.AUTH_USER_MODEL

class Admin(models.Model):
    admin_user_id = models.CharField(db_column='adminUserID', primary_key=True, max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='passWord', max_length=15)  # Field name made lowercase.

    class Meta:
        db_table = 'Admins'

    def __str__(self):
        return self.admin_user_id


class Member(models.Model):
    user_id = models.CharField(db_column='userID', primary_key=True, max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='passWord', max_length=15)  # Field name made lowercase.

    class Meta:
        db_table = 'Members'

    def __str__(self):
        return self.user_id


class Book(models.Model):
    book_id = models.IntegerField(db_column='bookID', primary_key=True)  # Field name made lowercase.
    borrower_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='borrowerID', blank=True, null=True, related_name='loans')  # Field name made lowercase.
    reserver_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='reserverID', blank=True, null=True, related_name='reservations')  # Field name made lowercase.
    start_date = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    due_date = models.DateField(db_column='dueDate', blank=True, null=True)  # Field name made lowercase.
    reserve_due_date = models.DateField(db_column='reserveDueDate', blank=True, null=True)  # Field name made lowercase.
    return_date = models.DateField(db_column='returnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        ordering = ['book_id']
        db_table = 'Books'

    def __str__(self):
        return str(self.book_id)

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book_details', args=[str(self.book_id)])

    @property
    def is_overdue(self):
        return timezone.now().date() > self.due_date


class Fine(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='userID', primary_key=True, related_name='fines')  # Field name made lowercase.
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'Fines'

    def __str__(self):
        return f'{self.user_id} owes ${self.amount} fine'


class Payment(models.Model):
    transaction_time = models.DateTimeField(db_column='transactionTime')  # Field name made lowercase.
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userID', related_name='payments')  # Field name made lowercase.
    amount = models.FloatField(db_column='paid', blank=True, null=True)
    card = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-transaction_time']
        db_table = 'Payments'

    def __str__(self):
        return f'{self.user_id} paid {self.amount} at {self.transaction_time}'
