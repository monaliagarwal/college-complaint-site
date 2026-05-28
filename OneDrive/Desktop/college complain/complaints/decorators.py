from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

# use these on views like @student_required
student_required = user_passes_test(is_student, login_url='/login/')
admin_required = user_passes_test(is_admin, login_url='/login/')