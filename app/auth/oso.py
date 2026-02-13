from oso import Oso
from app.models.user import User
from app.models.group_friends import GroupFriends
from app.models.user_groupf import UserGroupF
from app.auth import group_permissions
from app.auth.context import RequestContext  

oso = Oso()


def init_oso():
    # 1. Registrar las clases para que Polar las entienda
    oso.register_class(User)
    oso.register_class(GroupFriends)
    oso.register_class(UserGroupF)
    oso.register_class(RequestContext)



    oso.register_constant(group_permissions,"group_permissions")
    
    # 2. Cargar el archivo de políticas
    oso.load_files(["app/auth/policy.polar"])
    return oso


oso_instance = init_oso()

def get_oso():
    return oso_instance