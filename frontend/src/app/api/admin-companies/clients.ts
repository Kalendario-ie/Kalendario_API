import {CompanyConfig} from 'src/app/api/company-config/models';
import {companyConfigParser} from 'src/app/api/company-config/parsers';
import baseApiAxios from 'src/app/api/common/clients/base-api';
import {AdminCompany} from 'src/app/api/admin-companies/models';
import {adminCompanyParser} from 'src/app/api/admin-companies/parsers';
import baseModelRequest from 'src/app/api/common/clients/base-django-api';

const adminUrl = 'admin/companies/'
const stripeUrl = 'billing/accounts/';


export const adminCompanyClient = {
    ...baseModelRequest<AdminCompany, null>(adminUrl, adminCompanyParser),

    config(id: number, model: CompanyConfig): Promise<CompanyConfig> {
        return baseApiAxios.patch<CompanyConfig>(adminUrl + id + '/config/', model)
            .then(result => companyConfigParser(result.data));
    },

    stripeUrl(id: number): Promise<{ url: string }> {
        return baseApiAxios.post<{ url: string }>(`${stripeUrl}${id}/connect/`, {})
            .then(result => result.data);
    }
}

//
//   uploadProfilePicture(id: number, file: File): Observable<Company> {
//     const formData = new FormData();
//     formData.append('image', file);
//     return this.http.patch<Company>(this.baseUrl + id + '/photo/', formData)
//       .pipe(map(this.adapter.adapt));
//   }
//

//
//   stripeDetails(id: number): Observable<CompanyStripeDetails> {
//     return this.http.get<CompanyStripeDetails>(`${this.stripe}${id}/`).pipe(map(this.stripeAdapter.adapt));
//   }
// }

