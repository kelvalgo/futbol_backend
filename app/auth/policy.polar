# Un usuario puede visualizar los usuarios del grupo al que pertenece
# si es usurio de ese grupo

   
allow(ctx: RequestContext, "read", groupf: Group) if
    group_permissions.is_user_active(ctx) and
    (
        group_permissions.is_member_of_group(ctx, groupf) or
        group_permissions.is_admin_of_group(ctx, groupf)
    );

allow(ctx: RequestContext, "list_user_group", groupf: Group) if
    group_permissions.is_user_active(ctx) and
    (
        group_permissions.is_member_of_group(ctx, groupf) or
        group_permissions.is_admin_of_group(ctx, groupf)
    );

allow(ctx: RequestContext, "create_user", groupf: Group) if
    group_permissions.is_user_active(ctx) and
        (           
            group_permissions.is_admin_of_group(ctx, groupf)
        );    

allow(ctx: RequestContext, "read_all_users", groupf: Group) if
    group_permissions.is_user_active(ctx) and
        (           
            group_permissions.is_admin_of_group(ctx, groupf)
        );

allow(ctx: RequestContext, "change_password", _user: RequestContext) if
    group_permissions.is_user_active(ctx); 





allow(ctx: RequestContext, "create_invitation", groupf: Group) if
    group_permissions.is_user_active(ctx) and
        (           
            group_permissions.is_admin_of_group(ctx, groupf)
        );


allow(ctx: RequestContext, "accept_invitation", invitation: Invitation) if
    group_permissions.is_user_active(ctx) and
    (
        group_permissions.has_pending_invitation(ctx, invitation)
    );

allow(ctx: RequestContext, "reject_invitation", invitation: Invitation) if
    group_permissions.is_user_active(ctx) and
    (
        group_permissions.has_pending_invitation(ctx, invitation)
    );    



allow(ctx: RequestContext, "get_list_groups", _user: RequestContext) if
    group_permissions.is_user_active(ctx); 

allow(ctx: RequestContext, "new_group", _user: RequestContext) if
    group_permissions.is_user_active(ctx);     


    
 