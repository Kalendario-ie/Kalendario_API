import {adminPermissionGroupClient} from 'src/app/api/permissions';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminPermissionGroups';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore(storeName, adminPermissionGroupClient, (state) => state.adminPermissionGroups);


export {reducer as permissionGroupReducer}
export {actions as permissionGroupActions}
export {adapter as permissionGroupAdapter}
export {selectors as permissionGroupSelectors}
export {sagas as adminPermissionGroupSaga}

