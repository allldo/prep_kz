from django.contrib.auth import authenticate, login


def log_in(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False
