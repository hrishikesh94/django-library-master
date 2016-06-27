import csv
import sys
from django.core.management import setup_environ
from library import settings

setup_environ(settings)
from library_app.models import *


class Tee():
    with open('database.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=',')
        print spamreader.next
        
        for row in spamreader:
            print"\n"
            row = ', '.join(row)
            element = row.split(",")
            if element[1] == "None":
                print "entry number ="+element [0]
                print "title ="+ element [3]
                print "quantity ="+ element[4]
                print "catagory = "+element[2]
                print "ststus ="+element[5]
                entry = Component(title =element [3], catagory = Publisher.objects.get(name =element[2]), lend_period =LendPeriods.objects.get(title ="month"))
            else:
                             continue

sys.stdout = Tee(open("log.txt", "w"), sys.stdout)

print "done"
