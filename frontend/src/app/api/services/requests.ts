import * as yup from 'yup';

export interface UpsertServiceRequest {
    private: boolean;
    category: number;
    name: string;
    duration: string;
    cost: number;
    isFrom: boolean;
    description: string;
    color: string;
}

export const UpsertServiceRequestValidation = yup.object().shape({
    private: yup.boolean().required(),
    category: yup.number(),
    name: yup.string().required().max(255),
    duration: yup.string(),
    cost: yup.number(),
    description: yup.string().required().max(255),
    color: yup.string().required(),
});

export interface UpsertServiceCategoryRequest {
    name: string;
    color: string;
}

export const UpsertServiceCategoryRequestValidation = yup.object().shape({
    name: yup.string().required().max(255),
    color: yup.string().required(),
});
