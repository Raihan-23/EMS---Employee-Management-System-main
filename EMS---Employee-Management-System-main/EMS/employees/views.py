from .models import Employee
from django.shortcuts import render, redirect
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max

# Create your views here.

@login_required
def home(request):
    employees = Employee.objects.filter(is_active=True).order_by('-created_at')
    
    total_employee_count = employees.count()
    avg_salary = employees.aggregate(Avg('salary'))['salary__avg']
    total_distinct_designation = employees.values('designation').distinct().count()
    
    context = {
        'employees': employees,
        'total_employee_count': "{:,}".format(total_employee_count),
        'avg_salary': "{:,}".format(avg_salary),
        'total_distinct_designation': "{:,}".format(total_distinct_designation),
    }
    
    return render(request, 'home.html', context)

@login_required
def add_employee(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            address = request.POST.get('company')
            phone_number = request.POST.get('phone')
            salary = request.POST.get('salary')
            designation = request.POST.get('designation')
            description = request.POST.get('short_description')

            employee = Employee(
                name=name,
                address=address,
                phone_number=phone_number,
                salary=salary,
                designation=designation,
                description=description
            )
            employee.save()

            return render(request, 'add_employee.html', {'success': f"Employee Enrolled Sucessfully"})

        except ValueError as e:
            return render(request, 'add_employee.html', {'error': f"Value Error: {str(e)}"})

        except DatabaseError as e:
            return render(request, 'add_employee.html', {'error': f"Database Error: {str(e)}"})

        except Exception as e:
            return render(request, 'add_employee.html', {'error': f"An unexpected error occurred: {str(e)}"})

    max_id = Employee.objects.aggregate(Max('id'))['id__max']
    return render(request, 'add_employee.html', { 'employee_id': max_id + 1 })

@login_required
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        employee.is_active = False
        employee.save()    
    except Employee.DoesNotExist:
        return render(request, 'error-404.html', {'msg': 'Employee does not exist'})
    
    return redirect('home')
    
@login_required
def edit_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        if request.method == 'POST':
            name = request.POST.get('name')
            address = request.POST.get('company')
            phone = request.POST.get('phone')
            short_description = request.POST.get('short_description')

            try:
                employee.name = name
                employee.address = address
                employee.phone_number = phone
                employee.short_description = short_description
                employee.save()

            except ValueError as e:
                return render(request, 'edit_employee.html', {'employee': employee, 'error': f"Value Error: {str(e)}"})

            except DatabaseError as e:
                return render(request, 'edit_employee.html', {'employee': employee, 'error': f"Database Error: {str(e)}"})

            except Exception as e:
                return render(request, 'edit_employee.html', {'employee': employee, 'error': f"An unexpected error occurred: {str(e)}"})

            return render(request, 'add_employee.html', {'employee': employee, 'success': f"Employee Updated Sucessfully"})
        
    except Employee.DoesNotExist:
        return render(request, 'error-404.html', {'msg': 'Employee does not exist'})
    
    return render(request, 'edit_employee.html', {'employee': employee})

    

