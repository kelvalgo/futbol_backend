from fastapi import APIRouter,Depends,HTTPException,status
from app.filter.season_filter import SeasonFilter
from app.filter.group_filter import Group
from app.services.season_services import create_season_service, list_season_services, update_season_service
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.season import  SeasonRead,SeasonCreate,SeasonUpdatePatch
from app.auth.context import RequestContext
from oso import Oso
from app.auth.oso import get_oso
from app.core.enums.auth_results import AuthResult

router=APIRouter(prefix="/season", tags=["Season"])


@router.get("/id_group/{id_group}",response_model=list[SeasonRead], 
            status_code=status.HTTP_200_OK)
async def list_season(
    session: sessionDep,
    id_group:int,
    param:SeasonFilter= Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    Obtiene la lista de temporadas asociadas a un grupo específico.

    Este endpoint permite consultar las temporadas registradas para un grupo 
    utilizando el identificador del grupo (`id_group`). 

    La consulta admite filtros de paginación y otros parámetros definidos en `SeasonFilter`.

    Permisos:
    - El usuario debe tener autorización para ejecutar la acción `list_season`
    sobre el grupo consultado.  
    - La autorización se valida mediante el motor de políticas **Oso**.

    Parámetros:
    - **id_group**: Identificador del grupo del cual se desean listar las temporadas.
    - **param**: Filtros de búsqueda y paginación definidos en `SeasonFilter`.

    Respuestas:
    - **200**: Lista de temporadas del grupo.
    - **403**: El usuario no tiene permisos para consultar las temporadas del grupo.
    """

    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"list_season",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    return   list_season_services(session,id_group,param)


@router.post("/id_group/{id_group}/internal",
             status_code=status.HTTP_201_CREATED)
def create_season(id_group:int,                                 
                  session: sessionDep,
                  season_in:SeasonCreate= Depends(),  
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):   



    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if  oso.is_allowed(context,"create_season",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    return  create_season_service(session,id_group,season_in)



@router.patch("/groups/{group_id}/season/{id_season}internal",
    status_code=status.HTTP_200_OK
)
def update_season(session: sessionDep,
                 group_id:int,
                 id_season: int,
                 season_new:SeasonUpdatePatch,
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):     
    
    group = Group(id_group=group_id)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"update_season",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    return update_season_service(session,group_id,id_season,season_new)

   
    