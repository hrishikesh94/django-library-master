from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class Component(models.Model):
    """
    An Book class - to describe book in the system.
    """
    title = models.CharField(max_length=200)
    catagory = models.ForeignKey('Publisher')
    lend_period = models.ForeignKey('LendPeriods',default =1)
    lend_by = models.ManyToManyField('UserProfile',default=None,null=True,blank=True)
    lend_from = models.DateField(null=True, blank=True)
    total = models.IntegerField(max_length=100)
    issued = models.IntegerField(blank= True,null=True,default=0)
    remaining = models.IntegerField(blank= True,null=True,default=0)

    def __unicode__(self):
        return ' Component: ' + self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"


class ComponentIssue(models.Model):

    """
    Component issue class creating relation between users and components
    """
    user = models.ForeignKey('UserProfile')
    component=models.ForeignKey('Component')
    quantity =models.IntegerField(max_length=100,default=0)
    time = models.TimeField(default=timezone.now)

    def __unicode__(self):
        return 'Issued %s'%(str(self.user) + str(self.component))


class ReqestIssue(models.Model):
    user = models.ForeignKey(User)
    component=models.ForeignKey("Component")
    time = models.TimeField(default=timezone.now)

    def __unicode__(self):
        return 'Request %s: '%(str(self.user) + str(self.component))

# class Quantity(models.Model):
#     component = models.ForeignKey('Component')
#
#
#     class Meta:
#         ordering = ['component']
#         verbose_name = "Quantity"
#         verbose_name_plural = "Quantities"

class LendPeriods(models.Model):
    """
    Users can borrow books from library for different
    time period. This class defines frequently-used
    lending periods.
    """
    name = models.CharField(max_length=50)
    days_amount = models.IntegerField()

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        get_latest_by = "days_amount"
        ordering = ['days_amount']
        verbose_name = "Lending period"
        verbose_name_plural = "Lending periods"

class Publisher(models.Model):
    """
    Class defines book's publisher
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return 'Catagory : %s' % self.name

    class Meta:
        get_latest_by = "name"
        ordering = ['name']
        verbose_name = "Catagory"
        verbose_name_plural = "Catagories"


class RequestReturn(models.Model):
    """
    Model to raise a return request here
    """

    user = models.ForeignKey(User)
    component=models.ForeignKey("Component")


    def __unicode__(self):
        return 'RequestReturn %s'%(str(self.user) + str(self.component_id))


class UserProfile(models.Model):
    """
    Class provides more information according the system's users
    """
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    fb_name = models.CharField(max_length=60, null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True)
    join_date = models.DateField()

    def __unicode__(self):
        return self.user.username +'('+ self.user.first_name + ' ' + self.user.last_name+')'

    def gravator_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

    class Meta:
        get_latest_by = "join_date"
        ordering = ['user']
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

def get_or_create_userprofile(user):
    if user:
        # up = get_object_or_404(UserProfile, user=user)
        try:
            up = UserProfile.objects.get(user=user)
            if up:
                return up
        except ObjectDoesNotExist:
            pass
    up = UserProfile(user=user, join_date=timezone.now())
    up.save()
    return up


User.profile = property(lambda u: get_or_create_userprofile(user=u))
