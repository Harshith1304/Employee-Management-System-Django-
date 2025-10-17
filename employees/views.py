from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse

def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('employee_list')
    return render(request, 'login.html')

@login_required
def employee_list(request):
    search = request.GET.get('q', '')
    employees = Employee.objects.filter(name__icontains=search)
    return render(request, 'employee_list.html', {'employees': employees, 'search': search})

@login_required
def add_employee(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee_form.html', {'form': form})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Department', 'Role', 'Salary'])
    for emp in Employee.objects.all():
        writer.writerow([emp.name, emp.email, emp.department.name, emp.role, emp.salary])
    return response
