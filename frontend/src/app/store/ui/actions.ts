import {action} from 'typesafe-actions';
import {ACTION_TYPES} from './types';


export const setShowDashboardToggle = (value: boolean) =>
    action(ACTION_TYPES.SET_SHOW_DASHBOARD_TOGGLE, value)

export const toggleDashboardSidenav = () =>
    action(ACTION_TYPES.TOGGLE_DASHBOARD_SIDENAV)
