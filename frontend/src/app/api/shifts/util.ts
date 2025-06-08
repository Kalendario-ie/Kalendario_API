import {TimeFrame} from './models';


export function isAvailable(frame: TimeFrame, hour: number, minute: number) {
    const start = frame.start.hour + frame.start.minute / 60;
    const end = frame.end.hour + frame.end.minute / 60;
    const value = hour + minute / 60;
    return start <= value && end > value;
}
