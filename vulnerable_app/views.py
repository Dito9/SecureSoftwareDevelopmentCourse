"""
vulnerable_app/views.py

Aplicación Django con vulnerabilidades INTENCIONALES para laboratorio DAST.
Cada vulnerabilidad está mapeada al OWASP API Top 10.

⚠️  SOLO PARA FINES EDUCATIVOS — NO DESPLEGAR EN PRODUCCIÓN ⚠️
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import connection
import json


# ─────────────────────────────────────────────────────────────────────────────
# VULN #1 — OWASP API1: Broken Object Level Authorization (BOLA)
# Lista todos los usuarios sin requerir autenticación ni autorización.
# ZAP detecta: respuesta 200 con datos sensibles sin credenciales.
# ─────────────────────────────────────────────────────────────────────────────
def user_list(request):
    """
    VULNERABLE: expone todos los usuarios del sistema sin autenticación.
    Fix: agregar @login_required y filtrar solo datos del usuario propio.
    """
    users = list(User.objects.values(
        'id', 'username', 'email', 'is_staff', 'date_joined'
    ))
    return JsonResponse({'users': users})


# ─────────────────────────────────────────────────────────────────────────────
# VULN #2 — OWASP API3: Injection (XSS Reflejado)
# El parámetro ?q= se refleja en la respuesta sin sanitizar.
# ZAP detecta: payload <script>alert(1)</script> retornado sin escapar.
# ─────────────────────────────────────────────────────────────────────────────
def search(request):
    """
    VULNERABLE: el input del usuario se inyecta directamente en el HTML.
    Fix: usar Django templates con auto-escape, o json.dumps con Content-Type
    application/json.
    """
    query = request.GET.get('q', '')
    # ❌ Refleja el input sin escapar en HTML plano
    html = f"<html><body><p>Resultados para: {query}</p></body></html>"
    return HttpResponse(html, content_type='text/html')


# ─────────────────────────────────────────────────────────────────────────────
# VULN #3 — OWASP API8: Security Misconfiguration (Sin CSRF)
# Endpoint de escritura que acepta POST sin token CSRF.
# ZAP detecta: POST exitoso sin cabecera X-CSRFToken.
# ─────────────────────────────────────────────────────────────────────────────
@csrf_exempt  # ❌ Deshabilita la protección CSRF de Django
def transfer(request):
    """
    VULNERABLE: operación sensible sin protección CSRF.
    Fix: remover @csrf_exempt y enviar el token CSRF desde el frontend.
    """
    if request.method == 'POST':
        data = json.loads(request.body or '{}')
        amount = data.get('amount', 0)
        to_user = data.get('to', '')
        return JsonResponse({
            'status': 'transferred',
            'amount': amount,
            'to': to_user
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ─────────────────────────────────────────────────────────────────────────────
# VULN #4 — OWASP API3: Excessive Data Exposure
# El perfil devuelve campos internos que no deberían exponerse.
# ZAP detecta: respuesta con campos sensibles en endpoints no protegidos.
# ─────────────────────────────────────────────────────────────────────────────
def profile(request):
    """
    VULNERABLE: expone campos internos como is_staff y password hash.
    Fix: usar un serializer con allowlist explícita de campos públicos.
    """
    if not request.user.is_authenticated:
        # Incluso sin auth devuelve data del primer usuario como "demo"
        user = User.objects.first()
        if not user:
            return JsonResponse({'error': 'No users'}, status=404)
    else:
        user = request.user

    # ❌ Expone campos que no deberían ser públicos
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,          # campo interno
        'is_superuser': user.is_superuser,  # campo interno
        'password': user.password,           # hash de contraseña ❌❌❌
        'last_login': str(user.last_login),
    })


# ─────────────────────────────────────────────────────────────────────────────
# VULN #5 — OWASP API3: SQL Injection (raw query con input sin escapar)
# ZAP (Full Scan) detecta respuestas diferentes con payloads SQL.
# ─────────────────────────────────────────────────────────────────────────────
def user_by_id(request, user_id):
    """
    VULNERABLE: usa raw SQL con string interpolation.
    Fix: usar ORM de Django o parámetros preparados: User.objects.get(pk=user_id)
    """
    # ❌ Concatenación directa de input en query SQL
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, username, email FROM auth_user WHERE id = {user_id}")
        row = cursor.fetchone()

    if row:
        return JsonResponse({'id': row[0], 'username': row[1], 'email': row[2]})
    return JsonResponse({'error': 'User not found'}, status=404)


# ─────────────────────────────────────────────────────────────────────────────
# Vista de inicio — sin vulnerabilidades (para que ZAP tenga un punto de entrada)
# ─────────────────────────────────────────────────────────────────────────────
def index(request):
    return JsonResponse({
        'app': 'SecureSoftwareDevelopmentCourse - Lab DAST',
        'version': '1.0.0',
        'endpoints': [
            '/api/users/',
            '/api/search/?q=<query>',
            '/api/transfer/',
            '/api/profile/',
            '/api/users/<id>/',
        ]
    })
