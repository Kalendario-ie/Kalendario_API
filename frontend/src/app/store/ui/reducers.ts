import {Reducer} from 'redux';
import {ACTION_TYPES} from './types';
import {isMobile} from 'react-device-detect';


export interface UiState {
    showDashboardToggle: boolean;
    sidenavOpen: boolean;
}

const initialState: UiState = {
    showDashboardToggle: false,
    sidenavOpen: !isMobile,
}

const reducer: Reducer<UiState> = (state = initialState, {type, payload}) => {
    switch (type) {
        case ACTION_TYPES.SET_SHOW_DASHBOARD_TOGGLE:
            return {...state, showDashboardToggle: payload}
        case ACTION_TYPES.TOGGLE_DASHBOARD_SIDENAV:
            return {...state, sidenavOpen: !state.sidenavOpen}
        default:
            return {...state}
    }
}

export {reducer as uiReducer};
