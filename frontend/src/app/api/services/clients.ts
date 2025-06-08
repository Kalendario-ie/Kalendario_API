import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {serviceCategoryParser, serviceParser} from 'src/app/api/services/parsers';

const baseUrl = 'admin/services/';

export const adminServiceClient = {
    ...baseModelRequest(baseUrl, serviceParser),
}

export const adminServiceCategoryClient = {
    ...baseModelRequest('admin/serviceCategories/', serviceCategoryParser),
}
