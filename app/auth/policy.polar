# Un usuario puede visualizar los usuarios del grupo al que pertenece
# si es usurio de ese grupo

allow(ctx: RequestContext, "user", groupf:GroupFriends) if       
    group_permissions.is_user_active(ctx) and
    group_permissions.is_member_of_group(ctx, groupf);


# si es administrador de ese grupo
allow(ctx: RequestContext, "admin", groupf:GroupFriends) if   
    group_permissions.is_user_active(ctx) and
        (           
            group_permissions.is_admin_of_group(ctx, groupf)
        );
    
allow(ctx: RequestContext, "read", groupf: GroupFriends) if
    group_permissions.is_user_active(ctx) and
    (
        group_permissions.is_member_of_group(ctx, groupf) or
        group_permissions.is_admin_of_group(ctx, groupf)
    );

allow(ctx: RequestContext, "write", groupf: GroupFriends) if
    group_permissions.is_user_active(ctx) and
        (           
            group_permissions.is_admin_of_group(ctx, groupf)
        );

 