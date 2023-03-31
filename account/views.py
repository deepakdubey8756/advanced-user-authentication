from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import SignUpForm, LoginForm
import re
from utilities.genTokens import genToken
from utilities.passwordVlidator import validatePassword

@login_required
def index(request):
    user = request.user
    return render(request, 'registration/index.html', {"user": user})

def extract_email_details(request):
    """function to extract details to check if user exists"""
    message_content = "Everything is fine"

    email = request['email']
    password = request["password"]
    confirmPass = request["confirmPass"]
    r = re.split(r'[@\.]', email)
    username = '_'.join(r)
    status = not User.objects.filter(username=username).exists()
    if status == False:
        message_content = "Account already exits"
    return {"email": email,
            "password":password,
            "confirmPass": confirmPass,
            "username":username,
            "status":status,
            "message_content": message_content}


def create_user(details):
    """Create user profile and update detail's message and status """
    try:
        token = genToken()
        mail_status = send_mail(details['email'], token, "registration/email_templates.html", "email confirmation", "password_confirm")

        if mail_status['message_status']:
            #creating user and his profile
            user = User.objects.create_user(details['username'], details['email'], details['password'])
            user.save()
            profile = Profile(user = user, token=token, isVerfied = False)
            profile.save()
            
        details['message_content'] = mail_status['message_content']
        details['status'] = mail_status['message_status']

    except Exception as e:
        details['status'] = False
        details['message_content'] = e
    return details


def signup(request):
    """it will work as follows:
        1. Check if request is post and user isn't authenticated.
        2. else do other functionalities
        3. check if input data is valid.
        4. Check if user is already exists or not.
        5. if everything is fine then create user and send confimation email.
        6. else print error message.
        7. return the orignial form page
        """

    messages_content = "Please enter the details"
    message_status = messages.INFO

    if request.method  == 'POST' and not request.user.is_authenticated:
        
        form = SignUpForm(data = request.POST)
        details = extract_email_details(request.POST)

        password_status = validatePassword(details['confirmPass']) and validatePassword(details['password'])


        if password_status['status'] == False:
            details['status'] = False
            details['message_content'] = password_status['content']


        try:
            if form.is_valid() and details['status'] and details['confirmPass'] == details['password']:
                details = create_user(details)
            
            if  details['status'] :
                messages_content = "We have sended you verification email. Please verify."
                message_status = messages.SUCCESS
            else:
                    raise ValueError(details["message_content"])
                        
        except Exception as e:
            messages_content = e
            message_status = messages.ERROR
    
    if request.user.is_authenticated:
        return redirect('/')
    
    form = SignUpForm()
    messages.add_message(request, message_status, messages_content)
    return render(request, "registration/signup.html", {"form": form})


def confirmPass(request, token):
    """this function confirms verification and login user"""
    if request.user.is_authenticated:
        # print("User is authenticated", request.user)
        return redirect('/')
    try:
        # getting profile from token
        profile = Profile.objects.filter(token = str(token))
        if len(profile) == 0:
            messages.add_message(request, messages.ERROR, "Invalid token please do reset password to reconfirm your email")
            return redirect('accounts:login')
        
        #verifing user and changing authentication token
        # print("profile: ", profile)
        profile[0].isVerfied = True
        profile[0].token = "none"
        profile[0].save()

        #loging user and sending to home page.
        login(request, profile[0].user)
        messages.add_message(request, messages.SUCCESS, "Email successfully verified")
        return redirect('/')
    
    except Exception as e:
        print(e)
        return HttpResponse("Operation failed!", e)


def send_mail(user_email, token, template_str, subject, domain):
    """Take email and generate token to send it to user"""
    status = True
    message_content = "Everything is fine"
    try:
        template = render_to_string(template_str,{
            "token": token,
            "email": user_email,
            "protocol": "http",
            "domain": f"localhost:8000/accounts/{domain}"
        })
        
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.fail_silently = False
        email.send()
    except Exception as e:
        status = False
        message_content = e
    return {"message_status":status, "message_content": message_content}
    

def login_view(request):
    """Function to handle logging user"""
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user = request.user)
        if len(profile) == 0 or not profile[0].isVerfied:
            logout(request)
            messages.add_message(request, messages.ERROR, "Error login. verify your email")
            return redirect('accounts:reset')
        else:
            return redirect('/')
    
    message_status = messages.INFO
    message_content = ""
    if request.method == "POST" and not request.user.is_authenticated:
        email = request.POST['email']
        password  = request.POST['password']
        try:
            form = LoginForm(data = request.POST) and validatePassword(request.POST['password'])['status']
            if form.is_valid():
                user = User.objects.get(email=email)
                profile = Profile.objects.get(user = user)
                if not user.check_password(password):
                    raise ValueError("Enter the correct credentials")
                
                elif not profile.isVerfied:
                    messages.add_message(request, messages.ERROR, "Please verify your email")
                    return redirect("accounts:reset")
                else:
                    login(request, user)
                    return redirect("/")
            else:
                raise ValueError("Data is not valid")

        except Exception as e:
            message_status = messages.ERROR
            message_content = e
    
    messages.add_message(request, message_status, message_content)
    form = LoginForm()
    return render(request, "registration/login.html", {"form": form})
    

@login_required
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('accounts:login')
    return redirect('/')



def reset_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if len(user) == 0:
            messages.add_message(request, messages.ERROR, "User Not found! please enter correct email")
            return render(request, 'registration/pass_reset.html')
        
        status = []
        try:
             # print("Everything is fine till here......")
            profile = Profile.objects.filter(user = user[0])[0]
            token = genToken()
            profile.token = token
            profile.save()
            # print("Printing authentication token, ", profile.auth_token, 'token length', len(token))
            status = send_mail(email, str(token), "registration/reset_pass_email.html", "password reset", "resetconfirm")
        except Exception as e:
            status['message_status'] = False
        finally:
            if status['message_status']:
                messages.add_message(request, messages.SUCCESS, "We have sended you a email please follow along")
            else:
                messages.add_message(request, messages.ERROR, "Operation failed. Retry")
    return render(request, 'registration/pass_reset.html')


def reset_confirm(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    profile = Profile.objects.filter(token=str(token))
    # print(profile)
    if len(profile)==0:
        messages.add_message(request, messages.ERROR, "verificaiton failed. Retry")
        return redirect('accounts:reset')
    if request.method == 'POST':
        password = request.POST['password']
        confirmPass = request.POST['confirmPass']
        message_content = " "
        message_status = ""
        if len(password) <= 8:
            message_content = "length should be more than 8"
            message_status = messages.ERROR
        elif password != confirmPass:
            message_content = "passwords are not matching"
            message_status = messages.ERROR
        
        else:
            profile = profile[0]
            profile.isVerfied = True
            profile.token = "none"
            profile.save()
            user = profile.user
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "password reset sucessful. Please consider login")
            return redirect('/accounts/login')
        messages.add_message(request, message_status, message_content)
    return render(request, 'registration/password_reset.html', {'token': str(token)})
