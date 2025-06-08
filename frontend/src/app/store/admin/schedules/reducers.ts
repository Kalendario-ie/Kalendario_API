import {adminScheduleClient, Schedule} from 'src/app/api/schedule';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminSchedules';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore<Schedule>(storeName, adminScheduleClient, (state) => state.adminSchedules);

export {reducer as scheduleReducer}
export {actions as scheduleActions}
export {adapter as scheduleAdapter}
export {selectors as scheduleSelectors}
export {sagas as adminScheduleSaga}

