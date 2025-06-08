import {Moment} from 'moment';
import {IReadModel} from '../common/models';
import {CompanyConfig} from '../company-config/models';
import {Employee} from '../employees/models';
import {Service, ServiceCategory} from '../services/models';

export interface Company extends IReadModel {
    id: number;
    name: string;
    address: string;
    avatar: string;
    about: string;
    instagram: string;
    phoneNumber: string;
    whatsapp: string;
    facebook: string;
    config: CompanyConfig;
}

export interface CompanyDetails extends Company {
    employees: Employee[];
    services: Service[];
    serviceCategories: ServiceCategory[];
    config: CompanyConfig;
}

export interface Slot {
    id: number;
    date: string;
    start: Moment;
    end: Moment;
    title: string;
}
