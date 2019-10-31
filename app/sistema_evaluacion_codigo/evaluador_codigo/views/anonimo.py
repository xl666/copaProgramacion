# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from evaluador_codigo.decorators import logout_required
from evaluador_codigo.models import Academico, Alumno, Licenciatura, User, Equipo


@logout_required
def iniciar_sesion(request):
    context = {}
    template = "anonimo/login.html"
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        aut = authenticate(username=username, password=password)
        if aut is not None:
            usuario = User.objects.get(username=username)
            if not usuario.is_active:
                context["error"] = 'Su cuenta no está activa, porfavor contacte al administrador'
            else:
                login(request, aut)
                return redirect('inicio')
        else:
            context["error"] = 'Verifique usuario y contraseña'
        return render(request, template, context)

def hay_campos_vacios(listaCampos):
    campos = list(filter(lambda x: not x.strip() == '', listaCampos))
    return len(listaCampos) != len(campos)
    
@logout_required
def registrar_equipo(request):
    template = "anonimo/registro_equipo.html"
    context = {"licenciaturas": Licenciatura.objects.all()}
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        nombre_equipo = request.POST.get('nombreEquipo', '')
        nombre_maestro = request.POST.get('nombreMaestro', '')
        correo_maestro = request.POST.get('correoMaestro', '')
        nombre_alumno1 = request.POST.get('nombreAlumno1', '')
        correo_alumno1 = request.POST.get('correoAlumno1', '')
        nombre_alumno2 = request.POST.get('nombreAlumno2', '')
        correo_alumno2 = request.POST.get('correoAlumno2', '')
        nombre_alumno3 = request.POST.get('nombreAlumno3', '')
        correo_alumno3 = request.POST.get('correoAlumno3', '')
        universidad = request.POST.get('universidad', '')
        licenciatura = request.POST.get('licenciatura', '')
        ciudad = request.POST.get('ciudad', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('conf_password', '')

        if(hay_campos_vacios([nombre_equipo, nombre_maestro, correo_maestro, nombre_alumno1, correo_alumno1, nombre_alumno2, correo_alumno2, nombre_alumno3, correo_alumno3, universidad, licenciatura, ciudad, password1, password2])) :
            context["error"] = "Falta uno o más campos"
            return render(request, template, context)
        if password1 != password2:
            context["error"] = "La contraseña no coincide con su confirmación"
            return render(request, template, context)

        try:
            user = User.objects.create_user(username=nombre_equipo, first_name=nombre_equipo,
                                        last_name=nombre_equipo,
                                        password=password1, email=correo_maestro, is_student=True)
            lic = Licenciatura.objects.get(id=1)
            alumno = Alumno.objects.create(user=user, matricula='S100000', licenciatura=lic)
            Equipo.objects.create(alumno=alumno, nombre_equipo=nombre_equipo, nombre_maestro=nombre_maestro,
                                  correo_maestro=correo_maestro, nombre_alumno1=nombre_alumno1,
                                  correo_alumno1=correo_alumno1, nombre_alumno2=nombre_alumno2,
                                  correo_alumno2=correo_alumno2, nombre_alumno3=nombre_alumno3,
                                  correo_alumno3=correo_alumno3, universidad=universidad,
                                  licenciatura=licenciatura, ciudad=ciudad)
            context["exito"] = "Usuario " + user.username + " registrado exitosamente"
            return render(request, template, context)
        except Exception as e:
            print(e)
            context["error"] = "El usuario ya existe en el sistema"
            return render(request, template, context)
        
@logout_required
def registrar_alumno(request):
    template = "anonimo/registro_alumno.html"
    context = {"licenciaturas": Licenciatura.objects.all()}
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('name', None)
        last_name = request.POST.get('last_name', None)
        matricula = request.POST.get('matricula', None)
        id_licenciatura = request.POST.get('licenciatura', None)
        password = request.POST.get('password', None)
        conf_password = request.POST.get('conf_password', None)
        if not username.strip(' ') or not first_name.strip(' ') or not last_name.strip(' ') or not email.strip(' ') \
            or not matricula.strip(' ') or not password.strip(' ') or not conf_password.strip(
            ' ') or not id_licenciatura:
            context["error"] = "Falta uno o más campos"
            return render(request, template, context)
        elif password != conf_password:
            context["error"] = "La contraseña no coincide con su confirmación"
            return render(request, template, context)
        try:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password, email=email, is_student=True)
            lic = Licenciatura.objects.get(id=id_licenciatura)
            Alumno.objects.create(user=user, matricula=matricula, licenciatura=lic)
            context["exito"] = "Usuario " + user.username + " registrado exitosamente"
            return render(request, template, context)
        except:
            context["error"] = "El usuario ya existe en el sistema"
            return render(request, template, context)


@logout_required
def registrar_academico(request):
    template = "anonimo/registro_academico.html"
    context = {"licenciaturas": Licenciatura.objects.all()}
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('name', None)
        last_name = request.POST.get('last_name', None)
        id_licenciaturas = request.POST.getlist("licenciaturas")
        password = request.POST.get('password', None)
        conf_password = request.POST.get('conf_password', None)
        if not username.strip(' ') or not first_name.strip(' ') or not last_name.strip(' ') or not id_licenciaturas \
            or not email.strip(' ') or not password.strip(' ') or not conf_password.strip(' '):
            context["error"] = "Falta uno o más campos"
        elif password != conf_password:
            context["error"] = "La contraseña no coincide con su confirmación"
        else:
            try:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password, email=email, is_teacher=True, is_active=False)
                academico = Academico(user=user)
                academico.save()
                for id_licenciatura in id_licenciaturas:
                    lic = Licenciatura.objects.get(id=id_licenciatura)
                    academico.licenciaturas.add(lic)
                academico.save()
                context["exito"] = "Solicitud enviada exitosamente, el administrador le notificará cuando sea aceptada"
                return render(request, template, context)
            except:
                context["error"] = "El usuario ya existe en el sistema"
        return render(request, template, context)
