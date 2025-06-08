import baseApiAxios from 'src/app/api/common/clients/base-api';
import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {Permission} from 'src/app/api/permissions/models';
import {permissionGroupParser, permissionParser} from 'src/app/api/permissions/parsers';


const baseUrl = 'core/groups/';

export const adminPermissionGroupClient = {
    ...baseModelRequest(baseUrl, permissionGroupParser),
    permissions(): Promise<Permission[]> {
        return baseApiAxios
            .get<Permission[]>(baseUrl + 'permissions/')
            .then(result => result.data.map(permissionParser));
    }
}

