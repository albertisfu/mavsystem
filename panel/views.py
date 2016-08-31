from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# Create your views here.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
# acceso prohibido

@login_required
def prohibido(request):
    current_user = request.user
    us = post = get_object_or_404(User, username=current_user)
    return render(request, '403.html', {'user':us})