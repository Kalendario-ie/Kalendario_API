import * as yup from 'yup';




export interface UpsertUserRequest {
    firstName: string;
    lastName: string;
    email: string;
    employee: number | '';
    groups: number[];
}

export const UpsertUserRequestValidation = yup.object().shape({
    firstName: yup.string().required(),
    lastName: yup.string().required(),
    email: yup.string().required().email(),
});


export interface ChangeUserPasswordRequest {
    userPassword: string;
    password1: string;
    password2: string;
}

export const ChangeUserPasswordValidation = yup.object().shape({
    password1: yup.string().required(),
    password2: yup.string().required()
        .oneOf([yup.ref('password1'), null], 'Passwords must match'),
    userPassword: yup.string().required()
});
