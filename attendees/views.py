from django.shortcuts import render, redirect
from .forms import AttendeeForm

def register_attendee(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or another page
    else:
        form = AttendeeForm()
    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')
