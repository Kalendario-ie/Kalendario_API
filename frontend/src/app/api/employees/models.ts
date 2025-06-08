import {Person} from 'src/app/api/common/models';


export interface Employee extends Person {
    id: number;
    private: boolean;
    firstName: string;
    lastName: string;
    name: string;
    email: string;
    phone: string;
    schedule: number;
    instagram: string;
    photoUrl: string;
    bio: string;
    services: number[];
}


