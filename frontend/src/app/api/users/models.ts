import {IReadModel} from 'src/app/api/common/models';
import {getApp, PermissionModels} from '../common/permissions';


export function checkForPermission(user: AdminUser, permission: string, model: PermissionModels) {
    return user.permissions.includes(`${getApp(model)}.${permission}_${model}`);
}

export interface AdminUser extends IReadModel {
    firstName: string;
    lastName: string;
    email: string;
    employee: number | null;
    employeeId: number;
    groups: number[];
    permissions: string[];
    company: { id: number, name: string } | null;
    verified: boolean;
}




