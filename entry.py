import csv
import sys

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
                i =0
                while i< int(element[4]):
                    entry = Component(title =element [3], catagory = Publisher.objects.get(name =element[2]), lend_period =LendPeriods.objects.get(name ="month"))
                    entry.save()
                    i+=1
            else:
                             continue

sys.stdout = Tee(open("log.txt", "w"), sys.stdout)

print "done"
