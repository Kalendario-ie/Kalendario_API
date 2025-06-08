import {CustomerRequestAppointment} from 'src/app/api/appointments';
import {IReadModel} from 'src/app/api/common/models';
import {Company} from 'src/app/api/companies';
import {Employee} from 'src/app/api/employees';
import {AdminUser} from 'src/app/api/users';

export interface RequestItem {
  employee: Employee;
  appointments: CustomerRequestAppointment[];
}

export interface RequestModel extends IReadModel {
  id: number;
  owner: Company;
  name: string;
  scheduledDate: string;
  items: RequestItem[];
  itemsCount: number;
  total: number;
  complete: boolean;
  customerNotes: string | null | undefined;
  status: string;
  user: AdminUser;
}

