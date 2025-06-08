import {IReadModel} from 'src/app/api/common/models';
import {Shift} from '../shifts/models';

export interface Schedule extends IReadModel {
    mon: Shift;
    tue: Shift;
    wed: Shift;
    thu: Shift;
    fri: Shift;
    sat: Shift;
    sun: Shift;
    shifts: string[];
}


