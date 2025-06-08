import {createAction} from '@reduxjs/toolkit';
import {Moment} from 'moment';
import {momentToIso} from 'src/app/shared/util/moment-helpers';
import {adminDashboard} from 'src/app/store/admin/dashboard/state';

const setCurrentDate = createAction(
    `${adminDashboard}/setCurrentDate`,
    (value: Moment) => ({payload: momentToIso(value.startOf('day'))})
);

const setSelectedPanelId = createAction<number>(`${adminDashboard}/setCurrentPanel`);

export const actions = {
    setCurrentDate,
    setSelectedPanelId
}
