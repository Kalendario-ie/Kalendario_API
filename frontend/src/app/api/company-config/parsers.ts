import {PermissionModel} from 'src/app/api/auth';
import {CompanyConfig} from 'src/app/api/company-config/models';

export function companyConfigParser(data: any): CompanyConfig {
    return {
        ...data,
        name: data.id,
        permissionModel: PermissionModel.config
    }
}
