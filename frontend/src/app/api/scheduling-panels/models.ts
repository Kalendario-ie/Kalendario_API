import {IReadModel} from 'src/app/api/common/models';

export interface SchedulingPanel extends IReadModel {
    id: number;
    name: string;
    employees: number[];
}


