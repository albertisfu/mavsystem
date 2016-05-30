
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required

from django.conf import settings

def usuario(request):  #procesador de contexto, manda una variable a todos los templates
	if request.user.is_authenticated: #si la variable contiene datos de un usuario tenemos que verificar que este logueado para no causar errores en templates publicos
		try:
			current_user = request.user
			return {
            'usuario':current_user.first_name,
        }
		except:
			return {
            'usuario':"", #forzozamente se tiene que retornar algo
        }
