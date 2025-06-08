import * as yup from 'yup';

export interface UpsertPermissionGroupRequest {
  name: string;
  permissions: number[];
}


export interface UpsertPermissionRequest {
    id: number;
    name: string;
    codename: string;
}

export const UpsertPermissionRequestValidation = yup.object().shape({
    name: yup.string().required(),
    permissions: yup.array(yup.number()).required().min(1),
});
