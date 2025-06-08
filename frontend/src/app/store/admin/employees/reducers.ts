import {adminEmployeeClient} from 'src/app/api/employees';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminEmployees';

const {
    actions,
    adapter,
    reducer,
    sagas,
    slice,
    selectors
} = kCreateBaseStore(storeName, adminEmployeeClient, (state) => state.adminEmployees);

const reducerActions = slice.actions;

export {reducer as employeeReducer}
export {actions as employeeActions}
export {reducerActions as employeeReducerActions}
export {adapter as employeeAdapter}
export {selectors as employeeSelectors}
export {sagas as adminEmployeeSaga}

