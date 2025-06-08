import {adminAppointmentClient} from 'src/app/api/appointments';
import {kCreateBaseStore} from 'src/app/store/admin/common/adapter';

const storeName = 'adminAppointments';

const {
    actions,
    adapter,
    reducer,
    sagas,
    selectors
} = kCreateBaseStore(storeName, adminAppointmentClient, (state) => state.adminAppointments);

export {reducer as appointmentReducer}
export {actions as appointmentActions}
export {adapter as appointmentAdapter}
export {selectors as appointmentSelectors}
export {sagas as adminAppointmentSaga}

