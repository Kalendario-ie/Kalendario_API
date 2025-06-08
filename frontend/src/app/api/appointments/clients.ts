import {Appointment, AppointmentHistory} from 'src/app/api/appointments/models';
import {AppointmentQueryParams, UpsertCustomerAppointmentRequest} from 'src/app/api/appointments/requests';
import {ApiListResult} from 'src/app/api/common/api-results';
import baseApiAxios from 'src/app/api/common/clients/base-api';
import baseModelRequest from 'src/app/api/common/clients/base-django-api';
import {appointmentHistoryParser, appointmentParser, customerRequestAppointmentParser} from './parsers';

const adminUrl = 'admin/appointments/'
const userUrl = 'appointments/'

export const adminAppointmentClient = {
    ...baseModelRequest<Appointment, AppointmentQueryParams>(adminUrl, appointmentParser),
    history(id: number): Promise<ApiListResult<AppointmentHistory>> {
        return baseApiAxios.get<ApiListResult<AppointmentHistory>>(adminUrl + `${id}/history/`)
            .then(project => {
                project.data.results = project.data.results.map(appointmentHistoryParser);
                return project.data;
            });
    },

    createLock(model: any): Promise<Appointment> {
        return baseApiAxios.post<Appointment>(adminUrl + 'lock/', model)
            .then(result => customerRequestAppointmentParser(result.data));
    },

    updateLock(id: number, model: UpsertCustomerAppointmentRequest): Promise<Appointment> {
        return baseApiAxios.patch<Appointment>(adminUrl + `${id}/plock/`, model)
            .then(result => customerRequestAppointmentParser(result.data));
    }
}

export const appointmentClient = {
    ...baseModelRequest(userUrl, customerRequestAppointmentParser),
}
