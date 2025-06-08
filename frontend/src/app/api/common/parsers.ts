import {Person} from 'src/app/api/common/models';

export function personParser(data?: any): Person {

    return data ? {...data} : {
        id: 0, firstName: '',
        lastName: '',
        email: '',
        phone: ''
    }
}
