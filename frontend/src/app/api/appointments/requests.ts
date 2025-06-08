import {Moment} from 'moment';
import * as yup from 'yup';

export interface AppointmentQueryParams {
    status?: string;
    from_date?: string;
    to_date?: string;
    customer?: number;
    employee?: number;
    employees?: number[];
    services?: number[];
    show_all?: boolean;
    delete_only?: boolean;
}

export interface UpsertCustomerAppointmentRequest {
    start: string;
    end: string;
    customer: number;
    employee: number;
    service: number;
    internalNotes: string;
    ignoreAvailability: boolean;
}

export interface UpsertEmployeeEventRequest {
    start: string;
    end: string;
    employee: number;
    internalNotes: string | null;
    ignoreAvailability: boolean;
}

export const UpsertCustomerAppointmentRequestValidation = yup.object().shape({
    start: yup.date(),
    end: yup.date(),
    employee: yup.number().required(),
    customer: yup.number().required(),
    service: yup.number().required(),
    internalNotes: yup.string()
});

export const UpsertEmployeeEventRequestValidation = yup.object().shape({
    start: yup.date(),
    end: yup.date(),
    employee: yup.number().required(),
    internalNotes: yup.string().required()
});

export interface AdminAppointmentQueryParams {
    fromDate?: Moment;
    toDate?: Moment;
    customer?: number;
    employee?: number;
    employees?: number[];
    services?: number[];
}
