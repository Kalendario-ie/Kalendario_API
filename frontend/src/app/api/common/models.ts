import {PermissionModel} from 'src/app/api/auth';

export interface IReadModel {
    id: number;
    permissionModel: PermissionModel;
    name: string;
}

export interface Person extends IReadModel {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
}

export function modelId(model: IReadModel) {
    if (model) {
        return model.id;
    }
    return null;
}


function stringfy(value: number): string {
    if (value < 10) {
        return '0' + value.toString();
    }
    return value.toString();
}

export interface TimeOfDay {
    hour: number;
    minute: number;
}

export const Zero = () =>  ({hour: 0, minute: 0});

export const timeFromString = (time: string): TimeOfDay => {
    const timeOfDay = Zero();
    timeOfDay.hour = +time.substr(0, 2);
    timeOfDay.minute = +time.substr(3, 2);
    return timeOfDay;
}

export const timeToString = (t: TimeOfDay) => stringfy(t.hour) + ':' + stringfy(t.minute);

export const timeToISOString = (t: TimeOfDay) => stringfy(t.hour) + ':' + stringfy(t.minute) + ':00';

// hashCode(): number {
//     return this.hour + this.minute / 60;
// }
