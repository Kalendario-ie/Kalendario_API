import { all, fork } from 'redux-saga/effects'
import {adminAppointmentSaga} from 'src/app/store/admin/appointments';
import {adminCustomerSaga} from 'src/app/store/admin/customers';
import {adminEmployeeSaga} from 'src/app/store/admin/employees';
import {adminSchedulingPanelSaga} from 'src/app/store/admin/panels';
import {adminPermissionGroupSaga} from 'src/app/store/admin/permissionGroups';
import {adminPermissionsSagas} from 'src/app/store/admin/permissions';
import {adminScheduleSaga} from 'src/app/store/admin/schedules';
import {adminServiceCategorySaga} from 'src/app/store/admin/serviceCategories';
import {adminServiceSaga} from 'src/app/store/admin/services';
import {adminUserSaga} from 'src/app/store/admin/users';
import {userSaga} from 'src/app/store/users';
import {authSaga} from './auth';
import {companiesSaga} from './companies';


export function* rootSaga() {
    yield all([
        fork(authSaga),
        fork(companiesSaga),
        fork(userSaga),
        fork(adminServiceSaga),
        fork(adminServiceCategorySaga),
        fork(adminEmployeeSaga),
        fork(adminCustomerSaga),
        fork(adminScheduleSaga),
        fork(adminUserSaga),
        fork(adminPermissionGroupSaga),
        fork(adminPermissionsSagas),
        fork(adminAppointmentSaga),
        fork(adminSchedulingPanelSaga),
    ])
}
