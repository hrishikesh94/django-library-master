from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.template.base import add_to_builtins
from .forms import AuthenticateForm, UserCreateForm, UserEditForm, LendPeriodForm, BookForm, CatagoryForm
from .models import Component, LendPeriods, Publisher, UserProfile, ReqestIssue,ComponentIssue,RequestReturn
from .tables import BookTable, BookTableUser,  PublisherTable, PeriodsTable
from django_tables2 import RequestConfig
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators.group_required import group_required
from django.db.models.base import ObjectDoesNotExist
import django_tables2 as tables
from fandjango.decorators import facebook_authorization_required


add_to_builtins('library_app.templatetags.xextends')
add_to_builtins('library_app.templatetags.has_group')



def sign_in(request, auth_form=None):
    """
    View responsible for sign in using username and password
    (standard authorisation without facebook)

    :param auth_form: form that validates whether user can be authorized
    :type auth_form: `AuthenticationForm()`
    """
    username = password = " "

    if request.user.is_authenticated():
        redirect('/')

    if request.user.is_authenticated():
        redirect('/')
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        else:
            auth_form = auth_form or AuthenticateForm()
            return render(request, 'sign_in.html', {'auth_form': auth_form})
    auth_form = AuthenticateForm()
    return render(request, 'sign_in.html', {'auth_form': auth_form})


def sign_up(request, user_form=None, incomplete_form=None):
    """
    View responsible for sign up (without facebook authorization)

    :param user_form: for to validate input data and create new user (UserProfile and User)
    :type user_form: `UserCreateForm()`
    :param incomplete_form: (temporary) variable that determines whether the user_form contains errors
    :type incomplete_form: `string`
    """
    if request.method == 'POST' and incomplete_form is None:
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Form invalid")
            return sign_up(request, user_form=user_form, incomplete_form=True)
    if incomplete_form is None or not incomplete_form:
        user_form = UserCreateForm()
    return render(request, 'sign_up.html', {'user_form': user_form})


def logout_view(request):
    """
    View logs user out of the system.

    """
    logout(request)
    return redirect('/')


def home(request):
    """
    View for rendering home for both: authorized and unauthorized users.
    """
    if request.user.is_authenticated():
        # private home

        return render(request,
                      'home.html',
                      {'user': request.user,})
    else:
        # public home
        return render(request,
                      'public_home.html',
                      {'user': request.user})


def about(request):
    """
    Renders information about the system.
    """
    return render(request, 'about.html', {})


@login_required(login_url='/sign_in/')
def periods(request):
    """
    View allows users to search LendingPeriods.
    """
    periods_qs = LendPeriods.objects.all()
    return_dict = {}
    if request.method == 'POST':
        if request.POST['search'] and request.POST['keyword']:
            found_periods = LendPeriods.objects.filter(
                name__contains=request.POST['keyword'])

            periods_qs = found_periods
            return_dict['last_phrase'] = request.POST['keyword']

    periods_table = PeriodsTable(periods_qs)
    RequestConfig(request, paginate={"per_page": 5}).configure(periods_table)
    return_dict['periods_table'] = periods_table
    return render(request, 'periods.html', return_dict)


@login_required(login_url='/sign_in/')
def search_users(request):
    users_qs = UserProfile.objects.all()
    return_dict = {}
    if request.method == 'POST':
        if request.POST['search'] and request.POST['keyword']:
            found_users = UserProfile.objects.filter(
                user__name__contains=request.POST['keyword']) | UserProfile.objects.filter(
                user__surname__contains=request.POST['keyword'])

            users_qs = found_users
            return_dict['last_phrase'] = request.POST['keyword']

    return render(request, 'search_users.html', return_dict)




@group_required("Librarians")
def publishers(request):
    """
    View presents all book publishers present in the system.
    """
    publishers_qs = Publisher.objects.all()
    return_dict = {}
    if request.method == 'POST':
        if request.POST['search'] and request.POST['keyword']:
            found_publishers = Publisher.objects.filter(name__contains=request.POST['keyword'])

            publishers_qs = found_publishers
            return_dict['last_phrase'] = request.POST['keyword']

    publishers_table = PublisherTable(publishers_qs)
    RequestConfig(request, paginate={"per_page": 5}).configure(publishers_table)
    return_dict['publishers_table'] = publishers_table
    return render(request, 'publishers.html', return_dict)


@login_required(login_url='/sign_in/')
def books(request):
    """
    View presents all books present in the system.
    """
    books_qs = Component.objects.all()
    return_dict = {}
    if request.method == 'POST':
        if request.POST['search'] and request.POST['title_keyword'] and request.POST['where']:
            if request.POST['where'] == 'title':
                found_books = Component.objects.filter(title__contains=request.POST['title_keyword'])
            elif request.POST['where'] == 'author':
                found_books = Component.objects.filter(
                    author__name__contains=request.POST['title_keyword']) | Component.objects.filter(
                    author__surname__contains=request.POST['title_keyword'])
            else:  # searching in publishers
                found_books = Component.objects.filter(catagory__name__contains=request.POST['title_keyword'])

            if request.POST.get('only_available', False):
                found_books = found_books.filter(lend_by__isnull=True)
            books_qs = found_books
            return_dict['last_phrase'] = request.POST['title_keyword']
            return_dict['last_where'] = request.POST['where']

    books_table = BookTable(books_qs)
    RequestConfig(request, paginate={"per_page": 20}).configure(books_table)
    return_dict['books_table'] = books_table
    return render(request, 'books.html', return_dict)


@login_required(login_url='/sign_in/')
def books_show(request, book_id):
    """
    View presents specific book.

    :param book_id: id of the specific book
    :type book_id: `int`
    """
    try:
        book = Component.objects.get(id=book_id)
    except ObjectDoesNotExist:
        messages.error(request, "This component does not exist")
        return redirect('/')
    # if book.issued <= book.total:
    #     messages.error(request,"This component hasn't been issued by anyone! or has been successfully marked returned")
    #     return redirect('/books/')




    if book:
        book_list = ComponentIssue.objects.filter(component=book_id)
        books_qs = Component.objects.filter(id=book.id)
        books_table = BookTableUser(books_qs)

        return render(request, 'book_show.html',
                      {'book': book,
                       'books_table':books_table,
                       })
    else:
        return redirect('/books/')



@login_required(login_url='/sign_in/')
def publishers_show(request, publisher_id):
    """
    View presents specific publisher form the system.

    :param publisher_id: publisher's id
    :type publisher_id: `int`
    """
    try:
        publisher = Publisher.objects.get(id=publisher_id)
    except ObjectDoesNotExist:
        messages.error(request, "This publisher does not exist")
        return redirect('/')

    if publisher:
        books_qs = Component.objects.filter(publisher=publisher)
        books_table = BookTable(books_qs)
        RequestConfig(request, paginate={"per_page": 5}).configure(books_table)

        return render(request, 'publisher_show.html',
                      {'publisher': publisher,
                       'books_table': books_table,
                       'books_qs': books_qs})
    else:
        messages.info(request, "Publisher does not exist")
        return publishers(request)


@login_required(login_url='/sign_in/')
def periods_show(request, period_id):
    """
    View presents specific LendingPeriod.

    :param period_id: period's id
    :type period_id: `int`
    """
    try:
        period = LendPeriods.objects.get(id=period_id)
    except ObjectDoesNotExist:
        messages.error(request, "This period does not exist")
        return redirect('/')

    if period:
        return render(request, 'period_show.html',
                      {'period': period})
    else:
        messages.info(request, "Period does not exist")
        return periods(request)


@group_required('Librarians')
def remove_instance(request, what, id_obj):
    """
    View responsible for removing specific instance from the system.

    :param what: describes type of instance to remove e.g., authors, publishers, periods, books
    :type what: `string`
    :param id_obj: instance's id
    :type id_obj: `int`
    """
    if what == 'authors':
        what_singular = 'Author'

    elif what == 'publishers':
        what_singular = 'Publisher'
        obj = Publisher.objects.get(id=id_obj)
    elif what == 'periods':
        what_singular = 'Period'
        obj = LendPeriods.objects.get(id=id_obj)
    elif what == 'books':
        what_singular = 'Book'
        obj = Component.objects.get(id=id_obj)
    else:
        messages.info(request, "Incorrect type of instance...")
        return redirect('/')

    obj.delete()
    messages.success(request, what_singular + ' has been successfully removed')
    return redirect('/')


@group_required('Librarians')
def edit_instance(request, what, id_obj):
    """
    View responsible for editing specific instance from the system.

    :param what: describes type of instance to edit e.g., authors, publishers, periods, books
    :type what: `string`
    :param id_obj: instance's id
    :type id_obj: `int`
    """


    if what == 'publishers':
        what_singular = 'publisher'
        form = (CatagoryForm(request.POST,
                              instance=Publisher.objects.get(id=id_obj)) if request.method == 'POST' else CatagoryForm(
            instance=Publisher.objects.get(id=id_obj)))
    elif what == 'periods':
        what_singular = 'period'
        form = (
            LendPeriodForm(request.POST, instance=LendPeriods.objects.get(id=id_obj)) if request.method == 'POST' else
            LendPeriodForm(instance=LendPeriods.objects.get(id=id_obj)))
    elif what == 'books':
        what_singular = 'book'
        form = (BookForm(request.POST, instance=Component.objects.get(id=id_obj)) if request.method == 'POST' else BookForm(
            instance=Component.objects.get(id=id_obj)))
    else:
        messages.info(request, "Incorrect type of instance...")
        return redirect('/')

    title = 'Edit ' + what_singular

    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, what_singular + " has been edited.")
            return redirect('/')
        messages.info(request, "Incorrect or incomplete form")
    return render(request, 'new.html',
                  {'title': title,
                   'form': form,
                   'what': what,
                   'id_obj': id_obj})


@group_required('Librarians')
def create_instance(request, what):
    """
    View responsible for creating instance of specific type.

    :param what: describes type of instance to create e.g., authors, publishers, periods, books
    :type what: `string`
    """



    if what == 'publishers':
        what_singular = 'publisher'
        form = (CatagoryForm(request.POST) if request.method == 'POST' else CatagoryForm())
    elif what == 'periods':
        what_singular = 'period'
        form = (LendPeriodForm(request.POST) if request.method == 'POST' else LendPeriodForm())
    elif what == 'device':
        what_singular = 'device'
        form = (BookForm(request.POST) if request.method == 'POST' else BookForm())
    else:
        messages.info(request, "Incorrect type of new instance...")
        return redirect('/')

    title = 'Add new ' + what_singular

    if request.POST:
        if form.is_valid():
            form.lend_period = LendPeriods.objects.get(id =1)
            form.save()
            messages.success(request, "New " + what_singular + " has been added.")
            return redirect('/')
        messages.info(request, "Incorrect or incomplete form")
    return render(request, 'new.html',
                  {'title': title,
                   'form': form,
                   'what': what})


# this decorator also checks if user is authenticated

@login_required(login_url='/sign_in/')
def borrow_book(request, entry_id):
    """
    View responsible for marking that specific book has been borrowed and is not available in the library.

    :param book_id: book's id
    :type book_id: `int`
    """
    entry =ReqestIssue.objects.get(id=entry_id)
    book_id = entry.component_id
    user_id = entry.user_id
    book = Component.objects.get(id=book_id)

    if book:
        if book.issued < book.total:
            book.lend_by.add(UserProfile.objects.get(id=user_id))
            book.lend_from = timezone.now()
            book.issued += 1
            issue_case = ComponentIssue(component=book,user=UserProfile.objects.get(id=user_id))
            issue_case.save()
            book.save()
            ReqestIssue.objects.get(id = entry_id).delete()
    if book.issued == book.total:
        ReqestIssue.objects.filter(component_id=book_id).delete()
    return redirect('/books/request/approvals/')




@login_required(login_url='/sign_in/')
def return_book(request, entry_id):
    """
    View responsible for marking that specific component has been borrowed and is not available in the library.

    :param book_id: book's id
    :type book_id: `int`
    """
    book_id = RequestReturn.objects.get(id = entry_id).component_id
    user_id = RequestReturn.objects.get(id=entry_id).user_id
    total_quantity = 0
    entry = ComponentIssue.objects.filter(component=book_id,user_id = user_id)
    for sub in entry:
        total_quantity +=1
    entry.delete()
    book = Component.objects.get(id=book_id)
    if book:
        book.lend_by.remove(UserProfile.objects.get(user_id=user_id))
        book.issued -= total_quantity
        book.save()
        RequestReturn.objects.get(id = entry_id).delete()
    return redirect('/books/return/approvals/')



@login_required(login_url='/sign_in')
def request_borrow(request,book_id):
    """
    View responsible to make request to the admin about issuing any component
    :param rewuest:
    :param book_id:
    :return:
    """
    book = Component.objects.get(id=book_id)
    if book.issued != book.total:
        issue = ReqestIssue(user =request.user,component = book,time=timezone.now())
        issue.save()
        messages.success(request, 'component ' + book.title + ' has been registered under your name. Awaiting approval from Admin')
    return  redirect('/books/')



@login_required(login_url='/sign_in')
def requests_return(request,return_id):
    """
    View responsible to make request to the admin about issuing any component
    :param rewuest:
    :param book_id:
    :return:
    """
    book = Component.objects.get(id =return_id)
    if book.issued != book.total:
        issue = RequestReturn(user =request.user, component = book)
        issue.save()
        messages.success(request, 'component ' + book.title + ' has been registered for return under your name. Awaiting approval from Admin')
    return  redirect('/users/%s' %request.user)



@login_required(login_url='/sign_in')
def request_kill(request,entry_id):
    """
    View responsible to delete the selected request from one's list
    :param rewuest:
    :param book_id:
    :return:
    """
    ReqestIssue.objects.get(id=entry_id).delete()
    return  redirect('/books/request/all')


@login_required(login_url='/sign_in')
def requests_get(request):
    """
    view to get a list of all the requests that arent approved
    :param request:
    :return:
    """
    request_table= ReqestIssue.objects.all().order_by('time')
    return render(request,'show_requests.html',{'request_list':request_table})


@login_required(login_url='/sign_in')
def return_get(request):
    """
    view to get a list of all the requests for return arent approved
    :param request:
    :return:
    """
    request_table= RequestReturn.objects.all()
    return render(request,'show_returns.html',{'request_list':request_table})

@login_required(login_url='/sign_in')
def request_show(request):
    """
    view to get a list of all the requests that you have posted
    :param request:
    :return:
    """
    request_table= ReqestIssue.objects.filter(user=request.user)
    return render(request,'show_requests.html',{'request_list':request_table})


@login_required(login_url='/sign_in/')
def user(request, username):
    """
    View presents information connected with userprofile of specific user.

    :param username: username of user whom profile to render
    :param username: `string`
    """
    if request.user.username != username:
        other_user = True
    else:
        other_user = False
    try:
        this_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, "This user does not exist")
        redirect('/')

    profile = this_user.profile
    books_qs = Component.objects.filter(lend_by=profile)
    books_table = BookTableUser(books_qs)
    return render(request, 'user.html',
                  {'profile': profile,
                   'books_table': books_table,
                   'books_qs': books_qs,
                   })


@login_required(login_url='/sign_in/')
def user_connect(request, action, username):
    """
    View marks that two users of the system either become friends or
    has unfriended each other.

    :param action: describes which action has been undertaken, befirend or unfriend
    :type action: `string`
    :param username: describes which user is the subject of action (it's username)
    :type username: `string`
    :return:
    """
    try:
        other_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, "This user does not exist")
        redirect('/')

    if action == '1':
        # befriend
        str = 'befriended'
        request.user.profile.friends.add(other_user.profile)

    elif action == '0':
        # unfriend
        str = 'unfriended'
        request.user.profile.friends.remove(other_user.profile)
    else:
        messages.error(request, "Unknown action")
        redirect('/')

    request.user.profile.save()
    messages.success(request, "User successfully " + str)
    return user(request, request.user.username)


def return_view():
    pass


@login_required(login_url='/sign_in/')
def useredit(request, user_edit_form=None):
    """
    Allows to edit user preferences and data
    :param user_edit_form: form to edit user data
    :type user_edit_form: UserEditForm instance
    """
    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST)
        if user_edit_form.is_valid():
            user_edit_form.save(request.user)
            messages.success(request, 'Profile successfully edited!')
            return user(request, request.user.username)
        else:
            messages.error(request, 'Invalid form...')
            return render(request, 'useredit.html', {'user_edit_form': user_edit_form})
    else:
        user_edit_form = UserEditForm(initial={'username': request.user.username, 'email': request.user.email,
                                               'first_name': request.user.first_name,
                                               'last_name': request.user.last_name,
                                               'mobile': request.user.profile.mobile,
                                               'website': request.user.profile.website})
        return render(request, 'useredit.html', {'user_edit_form': user_edit_form})


@login_required(login_url='/sign_in/')
def change_password(request):
    """
    Responsible for changing user password
    """
    if request.method == 'POST':
        if check_password(request.POST['current_pass'], request.user.password):
            if request.POST['new_pass'] == request.POST['new_pass_confirm']:
                # passwords are the same
                messages.success(request, 'Password has been changed successfully, you need to login once again')
                request.user.set_password(request.POST['new_pass'])
                request.user.save()

                return redirect('/sign_in/')
            else:
                # different password
                messages.error(request, 'Passwords are different')
                return redirect('/change_password/')
        else:
            # incorrect password
            messages.error(request, 'Incorrect password')
            return redirect('/change_password')
    else:
        return render(request, 'change_password.html', {})
