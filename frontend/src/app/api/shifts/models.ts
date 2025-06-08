import {TimeOfDay} from 'src/app/api/common/models';

export interface TimeFrame {
    start: TimeOfDay;
    end: TimeOfDay;
    name: string;
}

export interface Shift {
    frames: TimeFrame[];
    name: string;
}




