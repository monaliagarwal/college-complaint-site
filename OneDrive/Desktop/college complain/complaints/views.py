from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint
from .decorators import student_required, admin_required
from .ai_helper import analyze_complaint


# ─── AUTH VIEWS ───────────────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']
        confirm  = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('student_dashboard')

    return render(request, 'complaints/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'complaints/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── STUDENT VIEWS ────────────────────────────────────────

@login_required
@student_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user

            urgency, summary = analyze_complaint(
                complaint.title,
                complaint.description
            )
            complaint.urgency    = urgency
            complaint.ai_summary = summary

            complaint.save()
            messages.success(request,
                f'Complaint submitted! AI flagged it as {urgency.upper()} urgency.')
            return redirect('student_dashboard')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/submit_complaint.html', {'form': form})


@login_required
@student_required
def student_dashboard(request):
    complaints = Complaint.objects.filter(student=request.user)

    total    = complaints.count()
    pending  = complaints.filter(status='pending').count()
    resolved = complaints.filter(status='resolved').count()

    context = {
        'complaints': complaints,
        'total':      total,
        'pending':    pending,
        'resolved':   resolved,
    }
    return render(request, 'complaints/student_dashboard.html', context)


# ─── ADMIN VIEWS ──────────────────────────────────────────

@login_required
@admin_required
def admin_dashboard(request):
    urgency_order = {'high': 0, 'medium': 1, 'low': 2}

    complaints = Complaint.objects.all().select_related('student')

    category_filter = request.GET.get('category', '')
    if category_filter:
        complaints = complaints.filter(category=category_filter)

    status_filter = request.GET.get('status', '')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    complaints = sorted(complaints,
                        key=lambda c: urgency_order.get(c.urgency, 3))

    total        = Complaint.objects.count()
    pending      = Complaint.objects.filter(status='pending').count()
    in_progress  = Complaint.objects.filter(status='in_progress').count()
    resolved     = Complaint.objects.filter(status='resolved').count()
    high_urgency = Complaint.objects.filter(urgency='high').count()

    context = {
        'complaints':      complaints,
        'total':           total,
        'pending':         pending,
        'in_progress':     in_progress,
        'resolved':        resolved,
        'high_urgency':    high_urgency,
        'category_filter': category_filter,
        'status_filter':   status_filter,
    }
    return render(request, 'complaints/admin_dashboard.html', context)


@login_required
@admin_required
def update_status(request, complaint_id):
    if request.method == 'POST':
        complaint = Complaint.objects.get(id=complaint_id)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'resolved']:
            complaint.status = new_status
            complaint.save()
            messages.success(request, f'Status updated to {new_status}')
    return redirect('admin_dashboard')


# ─── DETAIL VIEW ──────────────────────────────────────────

@login_required
def complaint_detail(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)

    if request.user != complaint.student and not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "You don't have permission to view this complaint.")
        return redirect('student_dashboard')

    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})
    