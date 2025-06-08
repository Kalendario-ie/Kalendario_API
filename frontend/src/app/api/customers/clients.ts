import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import { customerParser } from './parsers';

const baseUrl = 'admin/customers/';

export const adminCustomerClient = {
    ...baseModelRequest(baseUrl, customerParser)
}
