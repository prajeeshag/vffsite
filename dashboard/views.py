from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .forms import profileUpdateForm
from django.template import Context

# Create your views here.


@login_required()
def profile(request):
    if hasattr(request.user, 'profile'):
        form = profileUpdateForm(request.user)
        return render(request, 'dashboard/profile.html', {'form': form})
    else:
        if request.POST:
            form = profileUpdateForm(
                request.user, request.POST, files=request.FILES)
            if form.is_valid():
                profile = form.save()
                form = profileUpdateForm(request.user)
                return render(request, 'dashboard/profile.html', {'form': form})
        else:
            form = profileUpdateForm(request.user)
            return render(request, 'dashboard/profileUpdate.html', {'form': form})
