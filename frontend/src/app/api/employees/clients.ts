import baseApiAxios from 'src/app/api/common/clients/base-api';
import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import { employeeParser } from './parsers';

const baseUrl = 'admin/employees/';

export const adminEmployeeClient = {
    ...baseModelRequest(baseUrl, employeeParser),

    uploadProfilePicture(id: number, file: File): Promise<{ url: string }> {
        const formData = new FormData();
        formData.append('image', file);
        return baseApiAxios.post<{url: string}>(baseUrl + id + '/photo/', formData)
            .then(result => result.data);
    }
}
