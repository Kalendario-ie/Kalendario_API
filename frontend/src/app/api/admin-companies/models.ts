import {IReadModel} from 'src/app/api/common/models';
import {CompanyConfig} from 'src/app/api/company-config/models';

export interface CompanyStripeDetails extends IReadModel {
  detailsSubmitted: boolean;
  chargesEnabled: boolean;
  payoutsEnabled: boolean;
  defaultCurrency: boolean;
  requireConnect: boolean;
  currentlyDue: string[];
}

export interface AdminCompany extends IReadModel {
  address: string;
  avatar: string;
  about: string;
  instagram: string;
  phoneNumber: string;
  whatsapp: string;
  facebook: string;
  config: CompanyConfig;
}
