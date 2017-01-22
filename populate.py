import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'conf.settings')
import string
import django
django.setup()
from affirmation.models import Category,Page
import random
from affirmation.models import UserProfile, Data

from django.contrib.auth.models import User

def populate():

    USERS_NUM = 10
    NAMES1 = ["John","Ed","Mark","Allan","Jacob","Daniel","Charlie","Harry"]
    NAMES2 = ["Lucy","Anna","Claire","Heather","Alice","Rachel","Caitlyn","Louise"]
    
    users = []
    for i in range(0,USERS_NUM):
        roll1 = random.randint(-30,30)
        roll2 = roll1+random.randint(0,30)
        if (roll1>0):
            lname=NAMES1[roll1%len(NAMES1)]
            kname=NAMES2[roll2%len(NAMES2)]
            gen="Female"
            bgen="Male"
        elif (roll1<0):
            lname = NAMES2[roll1%len(NAMES2)]
            kname = NAMES1[roll2%len(NAMES1)]
            gen="Male"
            bgen="Female"
        else:
            names1=random.choice([NAMES1,NAMES2])
            names2=random.choice([NAMES1,NAMES2])
            lname=names1[roll1%len(names1)]
            kname=names2[roll2%len(names2)]
            gen=random.choice(["Male","Female"])
            bgen="Intersex"
            
        users.append(
            {
                'birthDate': "19"+str(random.randint(50,99))+"-"+"%02d"%(random.randint(1,12))+"-"+"%02d"%(random.randint(1,28)),
                'legalName': lname,
                'knownName': kname,
                'gender': gen,
                'birthGender': bgen,
            })

    data = {}
    for user in users:
        u=add_user(user)
        for j in range(random.randint(1,30)):
            d = "20"+"%02d"%(random.randint(15,16))+"-"+"%02d"%(random.randint(1,12))+"-"+"%02d"%(random.randint(1,28))
            s = random.randint(0,10)
            add_data(u,d,s)


def add_user(u):
    d,l,k,g,b = u["birthDate"], u["legalName"],u["knownName"],u["gender"],u["birthGender"]
    n,p = l[0]+k[0]+d[2:4], ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    a, created = User.objects.get_or_create(username=n)
    a.set_password(p)
    u, created = UserProfile.objects.get_or_create(birthDate=d, legalName=l, knownName=k, gender=g, birthGender=b,user_id=random.randint(0,1000000))
    a.save()
    u.save()
    print(n,p)
    return u

def add_data(user, date, sat):
    d, created = Data.objects.get_or_create(user=user,date=date,satisfaction=sat)
    d.save()
    return d

if __name__ == '__main__':
    populate()
