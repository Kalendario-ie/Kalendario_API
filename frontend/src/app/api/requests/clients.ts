import baseApiAxios from 'src/app/api/common/clients/base-api';
import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {RequestModel} from 'src/app/api/requests/models';
import {requestParser} from 'src/app/api/requests/parsers';

const baseUrl = 'admin/requests/';

export const adminRequestClient = {
    ...baseModelRequest(baseUrl, requestParser),

      accept: (id: number): Promise<RequestModel> => {
    return baseApiAxios.patch<RequestModel>(baseUrl + `${id}/accept/`, {})
        .then(result => requestParser(result.data));
  },

    reject: (id: number): Promise<RequestModel> => {
        return baseApiAxios.patch<RequestModel>(baseUrl + `${id}/reject/`, {})
            .then(result => requestParser(result.data));
    },
}

