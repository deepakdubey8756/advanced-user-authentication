from django.test import TestCase
from utilities.genTokens import genToken


class TestToken(TestCase):
    
    def test_gen_token(self):
        tokens = []
        for i in range(20):
            new_token = genToken()
            if new_token in tokens:
                self.assertTrue(False)
                return
            else:
                tokens.append(new_token)