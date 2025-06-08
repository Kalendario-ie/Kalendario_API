import {call, put, select, takeEvery} from 'redux-saga/effects';
import {Appointment, appointmentClient} from 'src/app/api/appointments';
import {ApiListResult} from 'src/app/api/common/api-results';
import {eventsRequestFail, eventsRequestSuccess} from 'src/app/store/users/actions';
import {selectEnd, selectStart} from 'src/app/store/users/selectors';
import {ACTION_TYPES} from 'src/app/store/users/types';


function* requestEvents(action: { type: string, payload: { start: string, end: string } }) {
    const start: string = yield select(selectStart);
    const end: string = yield select(selectEnd);
    if (start === action.payload.start && end === action.payload.end) {
        return;
    }
    try {
        const response: ApiListResult<Appointment> = yield call(appointmentClient.get, action.payload);
        yield put(eventsRequestSuccess(action.payload.start, action.payload.end, response.results));
    } catch (error) {
        yield put(eventsRequestFail(error));
    }
}

export function* userSaga() {
    yield takeEvery(ACTION_TYPES.EVENTS_REQUEST, requestEvents);
}
