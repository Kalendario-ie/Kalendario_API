import {createSelector} from '@reduxjs/toolkit';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';
import {schedulingPanelSelectors} from 'src/app/store/admin/panels';
import {RootState} from 'src/app/store/store';


const baseSelector = (state: RootState) => state.adminDashboard;

const selectCurrentDateString = createSelector(
    baseSelector,
    store => store.currentDate
)

const selectCurrentDate = createSelector(
    selectCurrentDateString,
    date => stringToMoment(date)
)

const selectSelectedPanelId = createSelector(
    baseSelector,
    store => store.selectedPanelId
)

const selectSelectedPanel = createSelector(
    (state) => state,
    selectSelectedPanelId,
    (state, id) => id ? schedulingPanelSelectors.selectById(state, id) : null
)

const selectPanelHours = createSelector(
    baseSelector,
    store => store.panelHours
)

const selectSlotSize = createSelector(
    baseSelector,
    store => store.slotSize
)


export const selectors = {
    selectCurrentDate,
    selectSelectedPanel,
    selectPanelHours,
    selectSlotSize
}
