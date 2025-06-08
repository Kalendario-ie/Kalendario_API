import {Moment} from 'moment';
import {HistoryType} from 'src/app/api/common/HistoryType';
import {IReadModel} from 'src/app/api/common/models';
import {Company} from 'src/app/api/companies';
import {Customer} from 'src/app/api/customers';
import {Employee} from 'src/app/api/employees/models';
import {Service} from 'src/app/api/services';
import {AdminUser} from 'src/app/api/users/models';

export enum EventType {
    EmployeeEvent,
    CustomerAppointment,
    CustomerRequestAppointment,
    CustomerEvent,
}

export type Appointment = CustomerEvent | CustomerRequestAppointment | CustomerAppointment | EmployeeEvent;

export interface CustomerEvent extends CustomerRequestAppointment {
    owner: Company;
}

export interface CustomerRequestAppointment extends CustomerAppointment {
    request: number;
    status: string;
    customerNotes: string;
    companyName: string;
    owner: number | Company;
}

export interface CustomerAppointment extends BaseAppointment {
    customer: Customer;
    service: Service;
}

export interface EmployeeEvent extends BaseAppointment {
    customer: null;
    service: null;
}

export interface BaseAppointment extends IReadModel {
    customer: Customer | null;
    service: Service | null;
    type: EventType;
    start: string;
    end: string;
    employee: Employee;
    owner: number | Company;
    internalNotes: string;
    customerNotes: string | null;
    deleted: string | null;
}

export interface History {
    historyType: HistoryType;
    historyDate: Moment | null;
    historyUser: AdminUser | null;
}

export type AppointmentHistory = Appointment & History;

