from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .forms import profileUpdateForm
# Create your views here.


@login_required()
def profile(request):
    if request.POST:
        form = profileUpdateForm(request.POST)
        if form.is_valid():
            profile = form.save()
            print("profile updated")
            print(profile)
    else:
        form = profileUpdateForm()
    return render(request, 'dashboard/profileUpdate.html', {'form': form})
    # return render(request, 'dashboard/profile.html')
