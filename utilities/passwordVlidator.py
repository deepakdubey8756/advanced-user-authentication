import re

def validatePassword(password):
    message = {"status": True, "content":"Everything fine"}

    if len(password) <= 8:
        message['status'] = False
        message['content'] = "Password should be more than 8 characters"

    elif re.search(r'[0-9]', password) == None:
        message['status'] = False
        message['content'] = 'Password should contain at least one number'

    elif re.search(r'[a-z]', password) == None:
        message['status'] = False
        message['content'] = 'Password should contain at least one lowercase character'
    
    elif re.search(r'[A-Z]', password) == None:
        message['status'] = False
        message['content'] = "Password should contain at least one uppercase character"
    
    elif re.search(r'\s', password) != None:
        message['status'] = False
        message['content'] = "No whitespace allowed"
    
    elif password.isalnum():
        message['status'] = False
        message['content'] = "Password should contain atleast one none alpha numberic character"
    
    return message

    
