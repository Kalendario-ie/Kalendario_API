import {appointmentParser} from 'src/app/api/appointments';
import {companyParser} from 'src/app/api/companies';
import {RequestItem, RequestModel} from 'src/app/api/requests';
import {userParser} from 'src/app/api/users';


export function requestParser(data: any): RequestModel {
    const items: {[key: string]: RequestItem} = {};
    let itemsCount = 0;
    for (const apt of data.appointments.map(appointmentParser)) {
        itemsCount += 1;
        if (items.hasOwnProperty(apt.employee.id)) {
            items[apt.employee.id].appointments.push(apt);
        } else {
            items[apt.employee.id] = {
                employee: apt.employee,
                appointments: [apt]
            };
        }
    }

    return {
        ...data,
        owner: companyParser(data.owner),
        user: data.user ? userParser(data.user) : null,
        name: data.user?.name,
        items: Object.keys(items).map(k => items[k]),
        itemsCount
    }

}
