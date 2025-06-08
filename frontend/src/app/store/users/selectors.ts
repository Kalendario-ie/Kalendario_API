import {createSelector} from '@reduxjs/toolkit';
import {RootState} from 'src/app/store/store';

const selectStore = (rootState: RootState) => rootState.users;

export const selectEvents = createSelector(
    [selectStore],
    (usersState) => usersState.events
)

export const selectStart = createSelector(
    [selectStore],
    (usersState) => usersState.start
)

export const selectEnd = createSelector(
    [selectStore],
    (usersState) => usersState.end
)

export const selectSelectedEvent = createSelector(
    [selectStore],
    (usersState) => usersState.selectedEvent
)
