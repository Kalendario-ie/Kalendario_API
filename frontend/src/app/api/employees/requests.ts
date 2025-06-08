import * as yup from 'yup';

export interface UpsertEmployeeRequest {
    private: boolean;
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    schedule: number;
    instagram: string;
    bio: string;
    services: number[];
}

export const UpsertEmployeeRequestValidation = yup.object().shape({
    firstName: yup.string().required('First Name is required'),
    lastName: yup.string().required('Last Name is required'),
    email: yup.string().required().email(),
    phone: yup.string().required(),
    services: yup.array(yup.number()).required().min(1)
});
