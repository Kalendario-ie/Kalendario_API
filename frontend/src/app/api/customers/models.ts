import {Person} from 'src/app/api/common/models';

export interface Customer extends Person {
    warning: string;
}
