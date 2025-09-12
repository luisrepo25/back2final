import json
from django.db import migrations
from django.contrib.auth.hashers import make_password

def load_initial_users(apps, schema_editor):
    Usuario = apps.get_model('authz', 'Usuario')
    Rol = apps.get_model('authz', 'Rol')
    with open('authz/initial_users.json', encoding='utf-8') as f:
        data = json.load(f)
        for user_data in data:
            roles = user_data.pop('roles', [])
            password = user_data.pop('password', None)
            # Verificar si el usuario ya existe por email
            if Usuario.objects.filter(email=user_data["email"]).exists():
                continue
            usuario = Usuario(
                nombres=user_data["nombres"],
                apellidos=user_data["apellidos"],
                email=user_data["email"],
                telefono=user_data.get("telefono"),
                estado=user_data["estado"]
            )
            if password:
                usuario.password = make_password(password)
            usuario.save()
            for rol_nombre in roles:
                rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)
                usuario.roles.add(rol)

class Migration(migrations.Migration):
    dependencies = [
        ('authz', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(load_initial_users),
    ]
