import {PermissionModel} from 'src/app/api/auth';
import {AdminUser} from 'src/app/api/users/models';
import {ChangeUserPasswordRequest, UpsertUserRequest} from 'src/app/api/users/requests';


export function userParser(data: any): AdminUser {
    return {
        ...data,
        permissionModel: PermissionModel.user,
    }
}

export function upsertUserRequestParser(user: AdminUser | null): UpsertUserRequest {
    return user ? {
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        employee: user.employeeId || '',
        groups: user.groups
    } : {
        firstName: '',
        lastName: '',
        email: '',
        employee: '',
        groups: []
    }
}

export function changeUserPasswordRequestParser(): ChangeUserPasswordRequest {
    return {
        password1: '', password2: '', userPassword: ''
    }
}
