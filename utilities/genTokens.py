import secrets

def genToken():
    """Functions to generate url safe tokens"""
    return secrets.token_urlsafe()