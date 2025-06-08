import {adminSchedulingPanelsClient} from 'src/app/api/scheduling-panels/clients';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminSchedulingPanels';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore(storeName, adminSchedulingPanelsClient, (state) => state.adminSchedulingPanels);

export {reducer as schedulingPanelReducer}
export {actions as schedulingPanelActions}
export {adapter as schedulingPanelAdapter}
export {selectors as schedulingPanelSelectors}
export {sagas as adminSchedulingPanelSaga}

