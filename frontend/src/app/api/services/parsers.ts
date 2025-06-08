import {PermissionModel} from 'src/app/api/auth';
import {timeFromString, timeToISOString} from 'src/app/api/common/models';
import {Service, ServiceCategory} from 'src/app/api/services/models';
import {UpsertServiceCategoryRequest, UpsertServiceRequest} from 'src/app/api/services/requests';


export function serviceParser(data?: any): Service {
    return {
        ...data,
        permissionModel: PermissionModel.service,
        duration: timeFromString(data.duration)
    }
}

export function serviceCategoryParser(data: any): ServiceCategory {
    return {
        ...data
    }
}

export function createUpsertServiceRequest(service: Service | null | undefined): UpsertServiceRequest {
    return service ? {
        private: service.private,
        category: service.category || 0,
        color: service.color,
        cost: service.cost,
        description: service.description,
        duration: timeToISOString(service.duration),
        isFrom: false,
        name: service.name
    } : {
        category: 0,
        color: '',
        cost: 0,
        description: '',
        duration: '',
        isFrom: false,
        name: '',
        private: false

    }
}

export function createUpsertServiceCategoryRequest(category: ServiceCategory | null | undefined): UpsertServiceCategoryRequest {
    return category ? {
        name: category.name,
        color: category.color || ''
    } : {
        name: '',
        color: '',
    }
}
