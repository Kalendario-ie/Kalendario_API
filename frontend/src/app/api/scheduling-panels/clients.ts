import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {schedulingPanelParser} from 'src/app/api/scheduling-panels/parsers';

const baseUrl = 'admin/panels/';

export const adminSchedulingPanelsClient = {
    ...baseModelRequest(baseUrl, schedulingPanelParser)
}
