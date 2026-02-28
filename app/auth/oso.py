from oso import Oso
from app.filter.group_filter import Group
from app.auth import group_permissions
from app.auth.context import RequestContext  
from app.filter.invitation_filter import Invitation

oso = Oso()


def init_oso():
    # 1. Registrar las clases para que Polar las entienda

    oso.register_class(RequestContext)
    oso.register_class(Invitation)
    oso.register_class(Group)
    

    

    oso.register_constant(group_permissions,"group_permissions")
    
    # 2. Cargar el archivo de políticas
    oso.load_files(["app/auth/policy.polar"])
    return oso


oso_instance = init_oso()

def get_oso():
    return oso_instance