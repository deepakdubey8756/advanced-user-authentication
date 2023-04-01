import re
def getUsername(email):
    r = re.split(r'[@\.]', email)
    username =  '_'.join(r)
    return username