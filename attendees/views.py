from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AttendeeForm
from .utils import get_db, send_otp
from bson.objectid import ObjectId
import qrcode
import io
import base64

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    # buffer.seek(0) -> optional, rewind the buffer to the beginning in case of errors
    return buffer.getvalue()

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
            attendee_id = db.attendees.insert_one(attendee_data).inserted_id

            # Generate the QR
            qr_code_data = str(attendee_id)
            qr_code_img = generate_qr(qr_code_data)

            # Saving the QR in database
            db.attendees.update_one({'_id': attendee_id}, {'$set': {'qr_code': qr_code_img}})

            return redirect('success', attendee_id=str(attendee_id))  # Redirect to success page
    else:
        form = AttendeeForm()

    return render(request, 'register.html', {'form': form})

def success(request, attendee_id):
    return render(request, 'success.html', {'attendee_id': attendee_id})

def verify_qr(request):
    message = None
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')

        if qr_code_data:
            try:
                db = get_db()
                attendee = db.attendees.find_one({'_id': ObjectId(qr_code_data)})
                
                if attendee:
                    message = f"Verified: {attendee['name']}"
                
                else:
                    message = "Verification failed"
            
            except Exception as e:
                message = "Error, please contact Ashmit or try again."
    
    return render(request, 'verify.html', {'message': message})

def view_qr(request, attendee_id):
    db = get_db()
    attendee = db.attendees.find_one({'_id': ObjectId(attendee_id)})
    
    if attendee and 'qr_code' in attendee:
        qr_code_img = attendee['qr_code']
        return HttpResponse(qr_code_img, content_type="image/png")
    else:
        return HttpResponse("QR code not found", status=404)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            send_otp(email)
            return render(request, 'login.html', {'message': 'OTP sent successfully', 'message_class': 'success'})
        except Exception as e:
            return render(request, 'login.html', {'message': 'Error sending OTP', 'message_class': 'error'})
    return render(request, 'login.html')
