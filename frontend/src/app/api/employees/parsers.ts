import {PermissionModel} from 'src/app/api/auth';
import {personParser} from 'src/app/api/common/parsers';
import {Employee} from 'src/app/api/employees/models';
import {UpsertEmployeeRequest} from 'src/app/api/employees/requests';

const imageStorage = process.env.REACT_APP_IMAGE_API_URL || 'https://res.cloudinary.com/gchahm/';

export function employeeParser(data?: any): Employee {
    return data ? {
        ...data,
        ...personParser(data),
        permissionModel: PermissionModel.employee,
        private: !!data.private,
        photoUrl: data.profileImg ? imageStorage + data.profileImg
            : 'img/default-avatar.jpg',
    } : {
        ...personParser(),
        private: false,
        photoUrl: null,
        instagram: '',
        schedule: 0,
        services: [],
    }

}


export function upsertEmployeeRequestParser(employee: Employee | null | undefined): UpsertEmployeeRequest {
    return employee ? {
        bio: employee.bio,
        email: employee.email,
        firstName: employee.firstName,
        instagram: employee.instagram,
        lastName: employee.lastName,
        phone: employee.phone,
        private: employee.private,
        schedule: employee.schedule,
        services: employee.services
    } : {
        bio: '',
        email: '',
        firstName: '',
        instagram: '',
        lastName: '',
        phone: '',
        private: false,
        schedule: 0,
        services: []
    }
}
