export {};
// import {createAction, createEntityAdapter, createSelector, createSlice, EntityState} from '@reduxjs/toolkit';
// import {call, put, select, takeEvery} from 'redux-saga/effects';
// import {adminAppointmentClient, Appointment, AppointmentQueryParams} from 'src/app/api/appointments';
// import {ApiBaseError} from 'src/app/api/common/api-errors';
// import {ApiListResult} from 'src/app/api/common/api-results';
// import {CreateActionPayload, PatchActionPayload} from 'src/app/store/admin/common/adapter';
// import {RootState} from 'src/app/store/store';
//
//
// interface State extends EntityState<Appointment> {
//     apiError: ApiBaseError | null;
//     editMode: boolean;
// }
//
// const sliceName = 'adminAppointments';
//
//
// const actions = {
//     fetchEntities: createAction<AppointmentQueryParams>(`${sliceName}/fetchEntities`),
//     createEntity: createAction<CreateActionPayload>(`${sliceName}/createEntity`),
//     patchEntity: createAction<PatchActionPayload>(`${sliceName}/patchEntity`),
//     deleteEntity: createAction<number>(`${sliceName}/deleteEntity`),
//     setEditMode: createAction<any>(`${sliceName}/setEditMode`),
// }
//
// const adapter = createEntityAdapter<Appointment>({
//     selectId: (entity) => entity.id,
//     sortComparer: (a, b) => a.name.localeCompare(b.name),
// })
//
// const slice = createSlice({
//     name: sliceName,
//     initialState: adapter.getInitialState({
//         apiError: null,
//         editMode: false
//     }) as State,
//     reducers: {
//         addMany: adapter.addMany,
//         upsertOne: adapter.upsertOne,
//         removeOne: adapter.removeOne,
//         setApiError: (state, action) => {
//             state.apiError = action.payload
//         },
//         setEditMode: (state, action) => {
//             state.editMode = action.payload;
//         }
//     }
// });
//
// const {reducer} = slice;
//
// const baseSelector = (state: RootState) => state.adminAppointments;
// const adapterSelectors = adapter.getSelectors(baseSelector);
//
// const selectors = {
//     ...adapterSelectors,
//     selectApiError: createSelector(baseSelector, store => store.apiError),
//     selectEditMode: createSelector(baseSelector, store => store.editMode),
// }
//
//
// function* fetchEntities(action: { type: string, payload: AppointmentQueryParams }) {
//     try {
//         const result: ApiListResult<Appointment> = yield call(adminAppointmentClient.get, action.payload);
//         yield put(slice.actions.addMany(result.results));
//     } catch (error) {
//         yield put(slice.actions.setApiError(error));
//     }
// }
//
// function* createEntity(action: { type: string, payload: CreateActionPayload }) {
//     try {
//         const entity: Appointment = yield call(adminAppointmentClient.post, action.payload.entity);
//         yield put(slice.actions.upsertOne(entity));
//         yield put(slice.actions.setApiError(null));
//         yield put(slice.actions.setEditMode(false));
//     } catch (error) {
//         yield put(slice.actions.setApiError(error));
//     }
// }
//
// function* patchEntity(action: { type: string, payload: PatchActionPayload }) {
//     try {
//         const entity: Appointment = yield call(adminAppointmentClient.patch, action.payload.id, action.payload.entity);
//         yield put(slice.actions.upsertOne(entity));
//         yield put(slice.actions.setApiError(null));
//         yield put(slice.actions.setEditMode(false));
//     } catch (error) {
//         yield put(slice.actions.setApiError(error));
//     }
// }
//
// function* deleteEntity(action: { type: string, payload: number }) {
//     try {
//         yield call(adminAppointmentClient.delete, action.payload);
//         yield put(slice.actions.removeOne(action.payload));
//         yield put(slice.actions.setApiError(null));
//     } catch (error) {
//         yield put(slice.actions.setApiError(error));
//     }
// }
//
// function* sagas() {
//     yield takeEvery(actions.fetchEntities.type, fetchEntities);
//     yield takeEvery(actions.createEntity.type, createEntity);
//     yield takeEvery(actions.patchEntity.type, patchEntity);
//     yield takeEvery(actions.deleteEntity.type, deleteEntity);
// }
//
// export {reducer as adminAppointmentReducer};
// export {actions as adminAppointmentActions};
// export {actions as adminAppointmentActions};
// export {sagas as adminAppointmentSagas};
//
