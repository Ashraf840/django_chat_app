from django.shortcuts import redirect

# Stop authenticated/ logged-in users
def stop_authenticated_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            return redirect('coreApp:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func