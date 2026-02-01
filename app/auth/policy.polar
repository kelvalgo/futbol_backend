# Un usuario puede visualizar los usuarios del grupo al que pertenece
# si es usurio de ese grupo

allow(user_id:Integer, "user", groupf_id:Integer) if
    group_permissions.is_member_of_group(user_id, groupf_id);

# si es administrador de ese grupo
allow(user_id:Integer, "admin", groupf_id:Integer) if
    group_permissions.is_admin_of_group(user_id, groupf_id);    