import {adminServiceCategoryClient, ServiceCategory} from 'src/app/api/services';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminServiceCategories';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore<ServiceCategory>(storeName, adminServiceCategoryClient, (state) => state.adminServiceCategories);

export {reducer as serviceCategoryReducer}
export {actions as serviceCategoryActions}
export {adapter as serviceCategoryAdapter}
export {selectors as serviceCategorySelectors}
export {sagas as adminServiceCategorySaga}

