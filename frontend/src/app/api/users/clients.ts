import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {AdminUser} from 'src/app/api/users/models';
import {userParser} from 'src/app/api/users/parsers';
import {ChangeUserPasswordRequest} from 'src/app/api/users/requests';
import baseApiAxios from 'src/app/api/common/clients/base-api';

const baseUrl = 'core/users/';

export const adminUserClient = {
    ...baseModelRequest(baseUrl, userParser),
    changePassword(id: number, model: ChangeUserPasswordRequest): Promise<AdminUser> {
        return baseApiAxios
            .patch<AdminUser>(baseUrl + id + '/changePassword/', model)
            .then(data => userParser(data.data));
    }
}
