from django.contrib import admin
from .models import Admin, Member, Book, Fine, Payment
from django.utils import timezone

# custom filter for Book
class BookOverdueListFilter(admin.SimpleListFilter):
    title = 'Overdue'
    parameter_name = 'overdue_days'

    def lookups(self, request, model_admin):
        return (('yes', 'Overdue'), ('no', ('Not overdue')))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(due_date__lt=timezone.now())
        elif self.value() == 'no':
            return queryset.filter(due_date__gte=timezone.now())

# custom admin model for Book, to show filters and display additional info
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'borrower_id', 'reserver_id', 'due_date', 'reserve_due_date')
    list_filter = (
        ('borrower_id', admin.EmptyFieldListFilter),
        ('reserver_id', admin.EmptyFieldListFilter),
        BookOverdueListFilter,
    )

# custom filter for Fine table
class UnpaidFineListFilter(admin.SimpleListFilter):
    title = 'Fine'
    parameter_name = 'amount'

    def lookups(self, request, model_admin):
        return (('paid', 'Paid'), ('unpaid', 'Unpaid'))

    def queryset(self, request, queryset):
        if self.value() == 'unpaid':
            return queryset.filter(amount__gt=0)
        elif self.value() == 'paid':
            return queryset.filter(amount=0)

class FineAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'amount')
    list_filter = (UnpaidFineListFilter,)

# custom model for Payment to display additional info
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_time', 'user_id', 'amount', 'card')

# Register your models here.
admin.site.register(Admin)

admin.site.register(Book, BookAdmin)    # custom admin model
admin.site.register(Fine, FineAdmin)
admin.site.register(Payment, PaymentAdmin)

admin.site.register(Member)
# admin.site.register(Book)
# admin.site.register(Fine)
# admin.site.register(Payment)