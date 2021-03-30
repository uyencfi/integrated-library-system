from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   # to decorate function
from django.contrib import messages
from django.utils import timezone
from .models import Book, Fine, Payment
from .forms import SearchForm, MakePaymentForm
from pymongo import MongoClient

mdb = MongoClient('localhost', 27017).Assignment1

def start(request):
    return render(request, 'start.html')

# intermediate class for home() below
class BookInfo():
    def __init__(self, b):
        self.book_id = b['_id']
        self.title = b['title']
        self.yearIndex = b['yearIndex']
        self.categories = ", ".join(b['categories'])
        # self.desc = b['shortDescription']
        self.authors = ", ".join(b['authors'])
        self.pages = b['pageCount']
        try:
            self.descLong = b['longDescription']
        except KeyError:
            self.descLong = "N.A."
        try:
            self.desc = b['shortDescription']
        except KeyError:
            self.desc = "N.A."
        try:
            self.isbn = b['isbn']
        except KeyError:
            self.isbn = "N.A."

@login_required
def home(request):
    # lst = [ x['_id'] for x in mdb.Books.find( { "$text": { "$search": keywords } } ) ]
    # books = Book.objects.filter(book_id__in=lst)
    # books = Book.objects.all()
    mdb = MongoClient('localhost', 27017).Assignment1
    books = []
    for b in mdb.Books.find():
        books.append(BookInfo(b))
    return render(request, 'home.html', {'books': books})

@login_required
def search(request):
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            mdb = MongoClient('localhost', 27017).Assignment1
            by_title = form.cleaned_data.get('by_title') # request.POST['by_title']
            by_year = form.cleaned_data.get('by_year') # request.POST['by_year']
            by_author = form.cleaned_data.get('by_author') # request.POST['by_author']
            by_category = form.cleaned_data.get('by_category') # request.POST['by_category']
            
            # basic search
            if not by_year and not by_author and not by_category:
                query = { "$text": { "$search": by_title } }
            else:
                conditions = [ {"$text": { "$search" : by_title } } ]
                # advanced search, at least 1 filter. Check which fields are non-empty
                if by_year:
                    a = by_year.split(", ")
                    for i in range(len(a)):
                        a[i] = int(a[i])
                    conditions.append({ "yearIndex" : { "$in" : a } })

                if by_author:
                    b = by_author.split(", ")
                    conditions.append({ "authors" : { "$in" : b } })
                
                if by_category:
                    c = by_category.split(", ")
                    conditions.append({ "categories" : { "$in" : c } })
                
                query = { "$and": conditions }
            result = []
            for b in mdb.Books.find(query):
                result.append(BookInfo(b))
            form = SearchForm()
            context['result'] = result
    else:
        context['result'] = 'GET'
        form = SearchForm()
    context['form'] = form
    return render(request, 'search.html', context)


def cancel_all_reservations(user):
    for i in user.reservations.all():
        i.reserver_id = None
        i.reserve_due_date = None
        i.save()

def USER_PROFILE_SCAN(user):
    # expired special reservation
    res = user.reservations.all()
    for x in res:
        if x.reserve_due_date and x.reserve_due_date < timezone.now().date():
            x.reserver_id = None
            x.reserve_due_date = None
            x.save()
    locked = status = False
    # check for any overdue books
    borrow = user.loans.all()
    for x in borrow:
        if x.is_overdue:
            cancel_all_reservations(user)
            # ONE TIME MSG: You have overdue books! All reservations cancelled. You cannot borrow or reserve.
            locked = status = True

    # check for unpaid fines
    if Fine.objects.filter(user_id=user).exists() and user.fines.amount != 0:
        # ONE TIME MSG: You have unpaid fines! All reservations cancelled. You cannot borrow or reserve.
        cancel_all_reservations(user)
        locked, status = True, False
    return (locked, status)

def check_eligibility(user, book):
    can_b = can_r = s_r = False
    if user.loans.all().count() == 4:
        msg = "You have reached the 4 book limit."
        if book.borrower_id == user:
            msg += " Also, you are borrowing this book!"
        elif book.reserver_id == user:
            msg += " Also, you are reserving this book!"
        elif book.reserver_id and book.reserver_id != user:
            msg += " No special reserve, as this book has been reserved."
        else:
            s_r = True
            msg = " This book can be reserved. You can do SPECIAL RESERVE."
    elif book.borrower_id:
        if book.borrower_id == user:
            msg = "You are already borrowing this book."
        elif book.reserver_id == user:
            msg = "You are already reserving this book."
        elif book.reserver_id != user:
            msg = "Sorry, this book has been borrowed and reserved."
        else:
            can_r = True
            msg = "This book has been borrowed by someone else but you can reserve it."
    else:
        can_b = True
        msg = "You can borrow this book."
    return (can_b, can_r, s_r, msg)

def book_details(request, book_id):
    # for book mongodb details
    mgbook = BookInfo(mdb.Books.find_one({"_id": book_id}) )
    # show buttons
    sqlbook = get_object_or_404(Book, book_id=book_id)
    if request.user.is_authenticated:
        locked, status = USER_PROFILE_SCAN(request.user)
        if locked:
            can_b, can_r, s_r = False, False, False
            if status:
                msg = "You have overdue books! All existing reservations are cancelled. You cannot borrow or reserve."
            else:
                msg = "You have unpaid fines! All existing reservations are cancelled. You cannot borrow or reserve."
        else:
            can_b, can_r, s_r, msg = check_eligibility(request.user, sqlbook)
        return render(
                request, 
                'book_details.html',
                {'can_b': can_b, 'can_r': can_r, 's_r': s_r, 'msg': msg, 'mgbook': mgbook, 'sqlbook': sqlbook}
            )
    return render(request, 'book_details.html', {'mgbook': mgbook, 'sqlbook': sqlbook})  


@login_required
def borrow(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if book.reserver_id == request.user:
        book.reserver_id = None
        book.reserve_due_date = None
    book.borrower_id = request.user
    book.start_date = timezone.now().date()
    book.due_date = book.start_date + timezone.timedelta(weeks=4)
    book.save()
    messages.success(request, "Book borrowed successfully.")
    # next = request.GET.get('next')
    # if next:
    #     return redirect(next)
    return redirect('book_details', book_id=book_id)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def reserve(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    book.reserver_id = request.user
    book.save()
    messages.success(request, "Book reserved successfully.")
    return redirect('book_details', book_id=book_id)

@login_required
def special_reserve(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    book.reserver_id = request.user
    book.reserve_due_date = timezone.now().date() + timezone.timedelta(weeks=1)
    book.save()
    messages.success(request, "Special reserve successful. Please note that if you do not borrow this book within 1 week, your reservation will be cancelled.")
    return redirect('book_details', book_id=book_id)


@login_required
def my_fines(request):
    user = request.user
    try:
        amount = Fine.objects.get(user_id=request.user).amount    # One on one relationship
    except Fine.DoesNotExist:
        amount = 0
    payment_history = user.payments
    return render(request, 'my_fines.html', {'amount': amount, 'payment_history': payment_history})

@login_required
def make_payment(request):
    try:
        curr_fine = Fine.objects.get(user_id=request.user)
    except Fine.DoesNotExist:
        messages.info(request, "You do not have any fines!")        
        return redirect('my_fines')
    if curr_fine.amount == 0:
        messages.info(request, "You do not have any fines!")
        return redirect('my_fines')
    if request.method == 'POST':
        form = MakePaymentForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                transaction_time=timezone.now(),
                user_id=request.user,
                amount=form.cleaned_data.get('amount'),
                card=form.cleaned_data.get('card_type'))
            payment.save()
            curr_fine.amount = max(curr_fine.amount - payment.amount, 0)
            curr_fine.save()
            messages.success(request, f'You successfully paid ${payment.amount}.')
            return redirect('my_fines')
    else:
        form = MakePaymentForm()
    return render(request, 'make_payment.html', {'form': form})


# intermediate class for my_books below
class MyBookInfo():
    def __init__(self, title, b):
        self.title = title
        self.b = b

@login_required
def my_books(request):
    borrow = request.user.loans.all()
    reservation = request.user.reservations.all()
    # get titles of my books
    my_borrow, my_reserve = [], []
    for b in borrow:
        title = mdb.Books.find_one({"_id": b.book_id})['title']
        my_borrow.append(MyBookInfo(title, b))
    for r in reservation:
        title = mdb.Books.find_one({"_id": r.book_id})['title']
        my_reserve.append(MyBookInfo(title, r))
    return render(request, 'my_books.html', {'my_borrow': my_borrow, 'my_reserve': my_reserve})

@login_required
def return_book(request, book_id):
    """Write return date. If overdue, increment fine. Clear borrower, due date, return date.
    If applicable, Update reserveDueDate i.e. grace period. Notify reserver_id."""
    book = get_object_or_404(Book, book_id=book_id)
    user = request.user
    if book.is_overdue:
        try:
            fine = Fine.objects.get(user_id=user)
        except Fine.DoesNotExist:
            fine = Fine.objects.create(user_id=user, amount=0)
        fine.amount += (timezone.now().date() - book.due_date).days
        fine.save()
    book.borrower_id = None
    book.due_date = None
    if book.reserver_id:
        book.due_date = timezone.now().date() + timezone.timedelta(weeks=1)
    book.save()
    messages.success(request, "Book returned successfully.")
    # NOTIFY RESERVER ID !!!!!!!!!!!! THEIR BOOK IS AVAILABLE
    return redirect('my_books')

@login_required
def extend(request, book_id):
    """Can extend if the book is not being reserved."""
    book = get_object_or_404(Book, book_id=book_id)
    if not book.reserver_id:
        book.due_date += timezone.timedelta(weeks=4)
        book.save()
        messages.success(request, "Extension successful.")
    else:
        messages.info(request, "Extension unsuccessful. Book is currently reserved for someone else.")
    return redirect('my_books')



    









