import datetime
import random
import socket

def citat():
    citaty = ("Nepřej si, aby to bylo snazší; přej si, abys byl lepší.","Budete-li se snažit porozumět celému vesmíru, nepochopíte vůbec nic. Jestliže se pokusíte porozumět sobě, pochopíte celý vesmír.")
    return str(random.choice(citaty))

def date():
    return str(datetime.date.today())

