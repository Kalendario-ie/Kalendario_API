import {PermissionModel} from 'src/app/api/auth';
import {IReadModel, TimeOfDay} from 'src/app/api/common/models';


export interface Service extends IReadModel {
    private: boolean;
    category: number | null;
    name: string;
    duration: TimeOfDay;
    color: string;
    description: string;
    cost: number;
    isFrom: boolean;
    price: string;
}

export interface ServiceCategory extends IReadModel {
    id: number;
    name: string;
    color?: string;
}

export const otherCategory = () => ({id: 0, name: 'Other', permissionModel: PermissionModel.servicecategory})
