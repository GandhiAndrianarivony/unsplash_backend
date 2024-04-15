import strawberry_django

from apps.users import models as u_models

@strawberry_django.interface(model=u_models.User)
class UserInterface:
    pass
