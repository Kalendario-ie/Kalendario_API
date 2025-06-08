import {Reducer} from 'redux';
import {CustomerEvent} from 'src/app/api/appointments';
import {ACTION_TYPES} from './types';


export interface UsersState {
    events: CustomerEvent[] | null;
    selectedEvent: CustomerEvent | null;
    start: string | null;
    end: string | null;
}

const initialState: UsersState = {
    events: null,
    selectedEvent: null,
    start: null,
    end: null
}

const reducer: Reducer<UsersState> = (state = initialState, {type, payload}) => {
    switch (type) {
        case ACTION_TYPES.EVENTS_REQUEST:
            return {...state}
        case ACTION_TYPES.EVENTS_REQUEST_SUCCESS:
            return {...state, ...payload}
        case ACTION_TYPES.SET_SELECTED_EVENT:
            return {...state, selectedEvent: payload}
        default:
            return {...state}
    }
}

export {reducer as usersReducer};
