from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Application, Userslogin, Section, Assignsection
from .decorators import session_required

def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Userslogin.objects.get(username=username)
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['userlogin'] = 'userlogin'
                request.session.set_expiry(300) 
                messages.success(request, 'Login successful.')
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password.')
        except Userslogin.DoesNotExist:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['userlogin'] = 'django_user'
                request.session.set_expiry(300)
                messages.success(request, 'Login successful.')
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@session_required
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        inpassword = request.POST.get('password1')
        cnfpassword = request.POST.get('password2')

        if inpassword != cnfpassword:
            messages.error(request, "Passwords do not match.")
        else:
            if Userslogin.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                Userslogin.objects.create(
                    username=username,
                    password=cnfpassword
                )
                messages.success(request, "User created successfully.")
                return redirect('login')

    return render(request, 'signup.html')

@session_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@session_required
def homepage(request):
    if request.session.get('userlogin') == 'django_user':
        applications = Application.objects.all()
        sections = Section.objects.all()
        all_sections = {}
        for section in sections:
            all_sections[section.name] = Application.objects.filter(section=section.name)
        return render(request, 'homepage.html', {'sections': all_sections})
    else:
        assigned_data = Assignsection.objects.filter(user__username=request.session.get('username')).first()
        if assigned_data:
            allowed_sections = assigned_data.sections.all()
            section_names = [section.name for section in allowed_sections]
            applications = Application.objects.filter(section__in=section_names)
        else:
            applications = []

        sections = {}
        for app in applications:
            if app.section not in sections:
                sections[app.section] = []
            sections[app.section].append(app)

        return render(request, 'homepage.html', {'sections': sections})

@session_required
def add_application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        link = request.POST.get('link')
        section_name = request.POST.get('section')

        try:
            Application.objects.create(name=name, photo=photo, link=link, section=section_name)
            messages.success(request, 'Link added successfully.')
            return redirect('homepage')
        except Exception as e:
            messages.error(request, f'Error adding application: {e}')

    sections = Section.objects.all()
    return render(request, 'add_application.html', {'sections': sections})

@session_required
def edit_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    sections = Section.objects.exclude(name=app.section)

    if request.method == 'POST':
        try:
            app.name = request.POST.get('name')
            if 'photo' in request.FILES:
                app.photo = request.FILES['photo']
            app.link = request.POST.get('link')
            app.section = request.POST.get('section')
            app.save()
            messages.success(request, 'Link updated successfully.')
            return redirect('homepage')
        except Exception as e:
            messages.error(request, f'Error updating link: {e}')

    return render(request, 'edit_application.html', {'app': app, 'sections': sections})

@session_required
def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    app.delete()
    messages.success(request, 'Link deleted successfully.')
    return redirect('homepage')

@session_required
def create_section(request):
    if request.method == 'POST':
        name = request.POST.get('sectionname')

        try:
            Section.objects.create(name=name)
            messages.success(request, 'Section created successfully.')
            return redirect('homepage')
        except Exception as e:
            messages.error(request, f'Error creating section: {e}')

    return render(request, 'create_section.html')

@session_required
def assign_sections(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sections = request.POST.getlist('sections')

        try:
            user = Userslogin.objects.get(username=username)
            assignsection, created = Assignsection.objects.get_or_create(
                user=user
            )
            section_objects = Section.objects.filter(name__in=sections)
            assignsection.sections.set(section_objects)
            
            messages.success(request, 'Sections assigned successfully.')
            return redirect('assign_sections')
        except Exception as e:
            messages.error(request, f'Error assigning sections: {e}')

    users = Userslogin.objects.values_list('username', flat=True)
    sections = Section.objects.values_list('name', flat=True)
    return render(request, 'assign_sections.html', {'users': users, 'sections': sections})

@session_required
def delete_section(request):
    sections = Section.objects.all()

    if request.method == 'POST':
        section_name = request.POST.get('section')
        section = get_object_or_404(Section, name=section_name)
        associated_links = Application.objects.filter(section=section_name)

        if 'confirm_delete' in request.POST:
            associated_links.delete()
            section.delete()
            messages.success(request, f'Section "{section_name}" and all associated links deleted successfully.')
            return redirect('delete_section')

        if associated_links.exists():
            return render(request, 'delete_section.html', {
                'sections': sections,
                'section_to_delete': section,
                'associated_links': associated_links,
                'confirm_delete': True
            })

        section.delete()
        messages.success(request, f'Section "{section_name}" deleted successfully.')
        return redirect('delete_section')

    return render(request, 'delete_section.html', {'sections': sections})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
