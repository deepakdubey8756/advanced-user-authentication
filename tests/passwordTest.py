from django.test import TestCase
from utilities.passValidator import validatePassword


#  message = {"status": True, "content":"Everything fine"}

#     if len(password) <= 8:
#         message['status'] = False
#         message['content'] = "Password should be more than 8 characters"

#     elif re.search(r'[0-9]', password) == None:
#         message['status'] = False
#         message['content'] = 'Password should contain at least one number'

#     elif re.search(r'[a-z]', password) == None:
#         message['status'] = False
#         message['content'] = 'Password should contain at least one lowercase character'
    
#     elif re.search(r'[A-Z]', password) == None:
#         message['status'] = False
#         message['content'] = "Password should contain at least one uppercase character"
    
#     elif re.search(r'\s', password) != None:
#         message['status'] = False
#         message['content'] = "No whitespace allowed"
    
#     elif password.isalnum():
#         message['status'] = False
#         message['content'] = "Password should contain atleast one non-alpha numberic character"
    

    


#Testing different utilities
class TestPassword(TestCase):

    def test_length(self):
        print("Testing length")
        message = validatePassword("test")
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], "Password should be more than 8 characters")
    
    def test_number(self):
        print("Testing Number")
        message = validatePassword("TestPasss")
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], "Password should contain at least one number")
    
    def test_lowercase(self):
        print("Testing LowerCase Character")
        message = validatePassword("TESTLOWERCASE101")
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], 'Password should contain at least one lowercase character')
    
    def test_upperCase(self):
        print("Testing UpperCase Character")
        message = validatePassword("testuppercase101")
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], 'Password should contain at least one uppercase character')

    
    def test_space(self):
        print("Testing space Character")
        message = validatePassword("Test Space101")
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], 'No whitespace allowed')


    def test_non_alpha_num(self):
        print("Testing non alpha numeric characters")
        message = validatePassword('TestNonAphaNumberic1')
        self.assertFalse(message['status'])
        self.assertEqual(message['content'], 'Password should contain atleast one non-alpha numberic character')

    def test_final(self):
        print("Testing final valid password")
        message = validatePassword("TestValid#Pass101")
        self.assertTrue(message['status'])
        self.assertEqual(message['content'], "Everything fine")



