import {AdminCompany, CompanyStripeDetails} from 'src/app/api/admin-companies/models';
import {PermissionModel} from 'src/app/api/auth';
import {companyConfigParser} from 'src/app/api/company-config/parsers';


export function companyStripeDetailsParser(data: any): CompanyStripeDetails {
    data = typeof data === 'object' ? data : {};
    return {
        ...data,
        id: data.ownerId,
        name: '',
        permissionModel: PermissionModel.company,
    }
}

export function adminCompanyParser(data: any): AdminCompany {
    data = typeof data === 'object' ? data : {};
    return {
        ...data,
        permissionModel: PermissionModel.company,
        config: data?.config ? companyConfigParser(data.config) : null
    }
}
