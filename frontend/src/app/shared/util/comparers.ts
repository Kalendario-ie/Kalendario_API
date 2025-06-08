import {BaseAppointment} from 'src/app/api/appointments';
import {IReadModel} from 'src/app/api/common/models';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';


export const compareByName = (a: IReadModel, b: IReadModel): number => {
    return a.name.localeCompare(b.name);
}

export const compareByStartDate = (a: BaseAppointment, b: BaseAppointment): number => {
    const aStart = stringToMoment(a.start);
    const bStart = stringToMoment(b.start);
    return aStart.diff(bStart);
}
