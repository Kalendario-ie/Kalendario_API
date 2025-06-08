import {adminUserClient} from 'src/app/api/users';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminUsers';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore(storeName, adminUserClient, (state) => state.adminUsers);

export {reducer as userReducer}
export {actions as userActions}
export {adapter as userAdapter}
export {selectors as userSelectors}
export {sagas as adminUserSaga}

