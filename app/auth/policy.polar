# Un usuario puede visualizar los usuarios del grupo al que pertenece
# si es usurio de ese grupo

allow(user:User, "user", groupf:GroupFriends) if       
    group_permissions.is_user_active(user) and
    group_permissions.is_member_of_group(user, groupf);


# si es administrador de ese grupo
allow(user:User, "admin", groupf:GroupFriends) if    
    group_permissions.is_user_active(user) and
    group_permissions.is_admin_of_group(user, groupf);    


allow(user: User, "read", groupf: GroupFriends) if
    group_permissions.is_user_active(user) and
    (
        group_permissions.is_member_of_group(user, groupf) or
        group_permissions.is_admin_of_group(user, groupf)
    );

allow(user: User, "write", groupf: GroupFriends) if
    group_permissions.is_user_active(user) and
    group_permissions.is_admin_of_group(user, groupf);

 