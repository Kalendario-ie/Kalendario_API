import {
  getApp,
  ModelPermissions,
  PERMISSION_ADD,
  PERMISSION_CHANGE,
  PERMISSION_DELETE,
  PERMISSION_VIEW,
  PermissionModels
} from './index';
import {AdminUser} from 'src/app/api/users';


export function userPermissions(user: AdminUser, model: PermissionModels): ModelPermissions {
  return {
    view: user.permissions.includes(`${getApp(model)}.${PERMISSION_VIEW}_${model}`),
    add: user.permissions.includes(`${getApp(model)}.${PERMISSION_ADD}_${model}`),
    change: user.permissions.includes(`${getApp(model)}.${PERMISSION_CHANGE}_${model}`),
    delete: user.permissions.includes(`${getApp(model)}.${PERMISSION_DELETE}_${model}`),
  };
}
//
// export function appointmentPermissions(user: IUser): AppointmentPermissions {
//   const model = Appointment.modelType;
//   return {
//     ...userPermissions(user, model),
//     overlap: user.permissionGroups.includes(`${getApp(model)}.overlap_${model}`),
//   };
// }
