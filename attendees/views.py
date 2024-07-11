from django.shortcuts import render, redirect
from .forms import AttendeeForm
from .utils import get_db

def register_attendee(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone']
            }
            db = get_db()
            db.attendees.insert_one(attendee_data)
            
            return redirect('success')  # Redirect to a success page or another page
    else:
        form = AttendeeForm()
    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')
