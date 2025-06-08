import {Moment} from 'moment';
import {PermissionModel} from 'src/app/api/auth';
import {timeToISOString} from 'src/app/api/common/models';
import {Schedule} from 'src/app/api/schedule/models';
import {UpsertScheduleRequest, UpsertScheduleRequestShift} from 'src/app/api/schedule/requests';
import {Shift, shiftParser} from 'src/app/api/shifts';

export function scheduleParser(data: any): Schedule {
    return {
        ...data,
        permissionModel: PermissionModel.schedule,
        mon: shiftParser(data.mon),
        tue: shiftParser(data.tue),
        wed: shiftParser(data.wed),
        thu: shiftParser(data.thu),
        fri: shiftParser(data.fri),
        sat: shiftParser(data.sat),
        sun: shiftParser(data.sun),
        shifts: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
    }
}

export function getShift(schedule: Schedule, date: Moment) {
    switch (date.isoWeekday()) {
        case 1:
            return schedule.mon;
        case 2:
            return schedule.tue;
        case 3:
            return schedule.wed;
        case 4:
            return schedule.thu;
        case 5:
            return schedule.fri;
        case 6:
            return schedule.sat;
        case 7:
            return schedule.sun;
    }
}

function shiftToUpsertShift(shift?: Shift): UpsertScheduleRequestShift {
    return shift ? {
        frames: shift.frames.map(frame => ({start: timeToISOString(frame.start), end: timeToISOString(frame.end)}))
    } : {frames: []};
}

export function upsertScheduleRequestParser(schedule: Schedule | null): UpsertScheduleRequest {
    return schedule ? {
        name: schedule.name,
        mon: shiftToUpsertShift(schedule.mon),
        tue: shiftToUpsertShift(schedule.tue),
        wed: shiftToUpsertShift(schedule.wed),
        thu: shiftToUpsertShift(schedule.thu),
        fri: shiftToUpsertShift(schedule.fri),
        sat: shiftToUpsertShift(schedule.sat),
        sun: shiftToUpsertShift(schedule.sun)

    } : {
        name: '',
        mon: {frames: []},
        tue: {frames: []},
        wed: {frames: []},
        thu: {frames: []},
        fri: {frames: []},
        sat: {frames: []},
        sun: {frames: []}
    }
}
