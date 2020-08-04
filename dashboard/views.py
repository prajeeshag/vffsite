from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .forms import profileUpdateForm
from django.template import Context

# Create your views here.


@login_required()
def profile(request):
    if request.POST:
        print(request.FILES)
        print(request.user)
        form = profileUpdateForm(
            request.user, request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            print("profile updated")
            print(profile)
        else:
            print(form.errors)
    else:
        print(request.user)
        form = profileUpdateForm(request.user)
        fld1 = form['profile_picture']
        context = Context({'field': fld1})
        context = context.flatten()
        print(context['field'].as_widget())
    return render(request, 'dashboard/profileUpdate.html', {'form': form})
    # return render(request, 'dashboard/profile.html')
