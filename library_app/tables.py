import django_tables2 as tables
from .models import Component, RequestReturn, Publisher, LendPeriods ,User,ComponentIssue
from datetime import timedelta, date


class PeriodsTable(tables.Table):
    """
    Table to render LendingPeriods from database
    """
    def render_name(self, record):
        return '<a href="/periods/show/%s">%s</a>' % (record.id, record.name)

    class Meta:
        model = LendPeriods
        attrs = {'class': 'books_table'}
        sequence = ('name', 'days_amount')
        fields = ('name', 'days_amount')


class PublisherTable(tables.Table):
    """
    Table to render Publishers from database
    """
    def render_name(self, record):
        return '<a href="/publishers/show/%s">%s</a>' % (record.id, record.name)

    class Meta:
        model = Publisher
        attrs = {'class': 'books_table'}
        sequence = ('name',)
        fields = ('name',)

class MotherBookTable(tables.Table):
    """
    Mother table to be inherited for all the books wala cases
    """




class BookTable(MotherBookTable):
    """
    Table to render Books from database
    """
    def user_type (self,record):
        name =User.objects.get(username= record.user).first_name
        return name.title()
    lend_period = tables.Column(verbose_name="Borrow")

    def render_title(self, record):

        return '<a href="/books/show/%d">%s</a>' % (record.id, record.title)


    def render_lend_period(self, record):
        if record.issued == record.total:
            return 'Already lent'
        else:
            return "<a href='/books/request/%s' onclick='javascript:return confirm(\"Do you want to borrow %s ?\")'>%s</a>" % (record.id, record.title, record.lend_period.__unicode__())
    def render_remaining(self,record):
        if record.issued == record.total:
            return 'None Leftt'
        else:
            return (int(record.total)-int(record.issued))

    class Meta:
        model = Component
        attrs = {'class': 'books_table'}
        sequence = ('title', 'catagory', 'lend_period','remaining','total','issued')
        fields = ('title', 'catagory', 'lend_period','remaining','total','issued')


class BookTableUser(MotherBookTable):
    """
    This table renders books, but is used to present
    books borrowed by the user and thus slightly differs from BookTable
    """
    lend_period = tables.Column(verbose_name="Need to return in")
    catagory = tables.Column(verbose_name="Need to return in")

    def render_lend_period(self, record):
        tekst = (record.lend_from + timedelta(days=record.lend_period.days_amount) - date.today()).__str__()[0:-9]
        if int(tekst[0:-5]) > 0:
            return '%s' % (record.lend_from + timedelta(days=record.lend_period.days_amount) - date.today()).__str__()[0:-9]
        else:
            return '<span class="deadline">Passed the deadline!</span>'

    def render_isseud(self,record):
        quantity = ComponentIssue.objects.filter(user=record.user.profile)
        total = 0
        for entry in quantity:
            total+=1
        return total

    def render_catagory(self,record):
                return "<a href='/books/request_return/%s' onclick='javascript:return confirm(\"Do you want to return %s ?\")'>Return Now</a>" % (record.id, record.title,)



    class Meta:
        model = ComponentIssue
        attrs = {'class': 'books_table'}
        sequence = ('title', 'lend_period','issued','catagory')
        fields = ('title', 'lend_period','issued','catagory')
