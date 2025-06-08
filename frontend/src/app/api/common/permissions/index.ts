export const PERMISSION_VIEW = 'view';
export const PERMISSION_ADD = 'add';
export const PERMISSION_CHANGE = 'change';
export const PERMISSION_DELETE = 'delete';

export interface ModelPermissions {
  view: boolean;
  add: boolean;
  change: boolean;
  delete: boolean;
}

export interface AppointmentPermissions extends ModelPermissions {
  overlap: boolean;
}

export enum PermissionModels {
  employee = 'employee',
  group = 'groupprofile',
  user = 'user',
  config = 'config',
  service = 'service',
  shift = 'shift',
  schedule = 'schedule',
  customer = 'customer',
  appointment = 'appointment',
  company = 'company'
}

export function getApp(permission: PermissionModels): string {
  switch (permission) {
    case PermissionModels.group:
      return 'core';
    case PermissionModels.user:
      return 'core';
    default:
      return 'scheduling';
  }
}


