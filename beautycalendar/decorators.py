from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def bussines_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
    Decorador para view que verifica que el usuario logueado sea bussines,
    si no, lleva a la pagina de login
    """
    actual_decorator= user_passes_test(
        lambda u: u.state== 1 and u.kind==1,
        login_url= login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

