from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'library.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#public urls
    url(r'^$', 'library_app.views.home', name='home'),
    url(r'^about/$', 'library_app.views.about', name='about'),
    url(r'^sign_in/$', 'library_app.views.sign_in', name='sign_in'),
    url(r'^sign_up/$', 'library_app.views.sign_up', name='sign_up'),
    url(r'^logout/$', 'library_app.views.logout_view', name='logout'),

    #books
    url(r'^books/$', 'library_app.views.books', name='books'),
    url(r'^books/show/(?P<book_id>\w{0,5})/$', 'library_app.views.books_show', name='books_show'),
    url(r'^books/borrow/(?P<entry_id>\w{0,5})/$', 'library_app.views.borrow_book', name='borrow_books'),
    url(r'^books/return/(?P<entry_id>\w{0,5})/$', 'library_app.views.return_book', name='return_book'),
    url(r'^books/request/approvals/$','library_app.views.requests_get',name='request_get'),
    url(r'^books/return/approvals/$','library_app.views.return_get',name='return_get'),
    url(r'^books/request/all/$','library_app.views.request_show',name='request_show'),
    url(r'^books/request/(?P<book_id>\w{0,5})/$','library_app.views.request_borrow',name='request_borrow'),
    url(r'^books/request/delete/(?P<entry_id>\w{0,5})/$','library_app.views.request_kill',name='request_kill'),
    url(r'^books/request_return/(?P<return_id>\w{0,5})/$','library_app.views.requests_return',name='request_return'),


    #users
    url(r'^change_password/$', 'library_app.views.change_password', name='change_password'),
    url(r'^users/$', 'library_app.views.search_users', name='search_users'),
    url(r'^users/(?P<action>\d{1})/(?P<username>\w{0,30})/$', 'library_app.views.user_connect', name='user_connect'),
    url(r'^users/(?P<username>\w{0,30})/$', 'library_app.views.user', name='user'),
    url(r'^useredit/$', 'library_app.views.useredit', name='useredit'),

    #publishers
    url(r'^publishers/$', 'library_app.views.publishers', name='publishers'),
    url(r'^publishers/show/(?P<publisher_id>\w{0,5})/$', 'library_app.views.publishers_show', name='publishers_show'),

    #periods
    url(r'^periods/$', 'library_app.views.periods', name='periods'),
    url(r'^periods/show/(?P<period_id>\w{0,5})/$', 'library_app.views.periods_show', name='periods_show'),

    #CRUD
    url(r'^(?P<what>\w{1,10})/new/$', 'library_app.views.create_instance', name='new'),
    url(r'^(?P<what>\w{1,10})/edit/(?P<id_obj>\d{1,10})$', 'library_app.views.edit_instance', name='edit'),
    url(r'^(?P<what>\w{1,10})/remove/(?P<id_obj>\d{1,10})$', 'library_app.views.remove_instance', name='remove'),

    url(r'^admin/', include(admin.site.urls)),

    #facebook
    # url(r'^fandjango/', include('fandjango.urls')),
    # url(r'^fb/(?P<what>\w{1,10})$', 'library_app.views.fb_sign_up', name='fb_sign_up'),
)

#static files
urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
