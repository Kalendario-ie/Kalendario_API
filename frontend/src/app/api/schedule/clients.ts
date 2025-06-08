import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {scheduleParser} from './parsers';

const baseUrl = 'admin/schedules/';

export const adminScheduleClient = {
    ...baseModelRequest(baseUrl, scheduleParser),
}
