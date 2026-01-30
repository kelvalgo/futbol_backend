# Un usuario puede listar usuarios de un grupo
# si es admin de ese grupo
allow(user_id:Integer, "user", groupf_id:Integer) if
    group_permissions.is_member_of_group(user_id, groupf_id);