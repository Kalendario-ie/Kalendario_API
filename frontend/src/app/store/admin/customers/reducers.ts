import {adminCustomerClient} from 'src/app/api/customers';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminCustomers';

const {
    actions,
    adapter,
    reducer,
    sagas,
    slice,
    selectors
} = kCreateBaseStore(storeName, adminCustomerClient, (state) => state.adminCustomers);

export {reducer as customerReducer}
export {actions as customerActions}
export {adapter as customerAdapter}
export {slice as customerSlice}
export {selectors as customerSelectors}
export {sagas as adminCustomerSaga}

