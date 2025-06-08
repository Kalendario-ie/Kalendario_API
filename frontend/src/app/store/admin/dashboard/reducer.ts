import {createReducer} from '@reduxjs/toolkit';
import {PayloadAction} from 'typesafe-actions';
import {actions} from './actions';
import {initialState} from './state';


export const reducer = createReducer(
    initialState,
    (builder) => {
        builder.addCase(actions.setCurrentDate.type, (state, action: PayloadAction<any, string>) => {
            state.currentDate = action.payload;
        });
        builder.addCase(actions.setSelectedPanelId.type, (state, action: PayloadAction<any, number>) => {
            state.selectedPanelId = action.payload;
        });
    }
)
