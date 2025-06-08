import {timeFromString, timeToString} from 'src/app/api/common/models';
import {Shift, TimeFrame} from 'src/app/api/shifts/models';


export function shiftParser(data: any): Shift {
    const frames: TimeFrame[] = data?.frames ? data.frames.map((f: any) => timeFrameParser(f.start, f.end)) : [];
    return {
        frames,
        name: frames.length > 0 ? frames.map(f => f.name).reduce(((p, c) => `${p} ${c}`)) : ''
    }
}

export function timeFrameParser(start: string, end: string): TimeFrame {
    const startTod = timeFromString(start);
    const endTod = timeFromString(end);
    return {
        start: startTod,
        end: endTod,
        name: timeToString(startTod) + ' - ' + timeToString(endTod)
    }
}
