import moment from 'moment';
import {companyConfigParser} from 'src/app/api/company-config/parsers';
import {otherCategory, serviceCategoryParser, serviceParser} from 'src/app/api/services';
import {employeeParser} from '../employees';
import {Company, CompanyDetails, Slot} from './models';

const imageStorage = process.env.REACT_APP_IMAGE_API_URL || 'https://res.cloudinary.com/gchahm/';

export function companyDetailsParser(data: any): CompanyDetails {
    let hasOtherCategory = false;
    const services = data.services.map((service: any) => {
        if (!service.category) {
            hasOtherCategory = true;
        }
        return serviceParser(service);
    });
    const serviceCategories = data.serviceCategories.map((cat: any) => serviceCategoryParser(cat));
    if (hasOtherCategory) {
        serviceCategories.push(otherCategory());
    }
    return {
        ...data,
        avatar: imageStorage + data.avatar,
        employees: data.employees.map((employee: any) => employeeParser(employee)),
        services: services,
        serviceCategories: serviceCategories,
        config: companyConfigParser(data.config)
    }
}

export function companyParser(data: any): Company {
    return {
        ...data,
        avatar: imageStorage + data.avatar,
        config: companyConfigParser(data.config)
    }
}


export function slotParser(id: number, data: any): Slot {
    const start = moment.utc(data.start);
    const end = moment.utc(data.end);
    return {
        id,
        date: start.clone().startOf('day').toISOString(),
        start,
        end,
        title: start.format('HH:mm') + ' - ' + end.format('HH:mm'),
    }
}
