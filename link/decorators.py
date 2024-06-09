from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def session_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You need to log in first.')
        return redirect('login')
    return _wrapped_view
