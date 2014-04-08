from flask.ext.principal import Permission, RoleNeed

user_permission = Permission(RoleNeed('user'))
admin_permission = Permission(RoleNeed('admin'))
