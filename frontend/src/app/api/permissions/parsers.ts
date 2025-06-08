import {PermissionModel} from 'src/app/api/auth';
import {Permission, PermissionGroup} from 'src/app/api/permissions/models';
import {UpsertPermissionGroupRequest} from 'src/app/api/permissions/requests';


export function permissionGroupParser(data: any): PermissionGroup {
    return {
        ...data,
        permissionModel: PermissionModel.groupprofile,
        permissions: data.permissions ? data.permissions : []
    }
}

export function permissionParser(data: any): Permission {
    return {
        ...data,
    }
}

export function upsertPermissionGroupRequestParser(permissionGroup: PermissionGroup | null): UpsertPermissionGroupRequest {
    return permissionGroup ? {
        name: permissionGroup.name,
        permissions: permissionGroup.permissions
    } : {
        name: '',
        permissions: []
    }
}
