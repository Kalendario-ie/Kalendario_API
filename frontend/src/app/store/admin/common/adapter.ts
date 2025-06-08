import {
    ActionCreatorWithoutPayload,
    ActionCreatorWithPayload,
    createAction,
    createEntityAdapter,
    createSelector,
    createSlice, Dictionary,
    EntitySelectors,
    EntityState,
    OutputParametricSelector
} from '@reduxjs/toolkit';
import {call, put, select, takeEvery} from 'redux-saga/effects';
import {ApiBaseError} from 'src/app/api/common/api-errors';
import {ApiListResult} from 'src/app/api/common/api-results';
import {BaseModelRequest} from 'src/app/api/common/clients/base-django-api';
import {IReadModel} from 'src/app/api/common/models';
import {compareByName} from 'src/app/shared/util/comparers';
import {PayloadAction} from 'typesafe-actions';


interface BaseState<TEntity> extends EntityState<TEntity> {
    isInitialized: boolean;
    isLoading: boolean;
    apiError: ApiBaseError | null;
    editMode: boolean;
    createdEntityId: number | null;
}

export interface BaseSelectors<TEntity> extends EntitySelectors<TEntity, any> {
    selectByIds: OutputParametricSelector<any, number[], NonNullable<TEntity>[], (res1: Dictionary<TEntity>, res2: number[]) => NonNullable<TEntity>[]>
    selectIsInitialized: (state: any) => boolean;
    selectApiError: (state: any) => ApiBaseError | null;
    selectEditMode: (state: any) => boolean;
    selectIsLoading: (state: any) => boolean;
    selectCreatedEntity: (state: any) => TEntity | undefined;
}

export interface PatchActionPayload {
    id: number,
    entity: any
}

export interface CreateActionPayload {
    entity: any
}

export interface BaseActions {
    initializeStore: ActionCreatorWithoutPayload;
    fetchEntities: ActionCreatorWithPayload<object>;
    fetchEntity: ActionCreatorWithPayload<number>;
    fetchEntitiesWithSetAll: ActionCreatorWithPayload<object>;
    createEntity: ActionCreatorWithPayload<CreateActionPayload>;
    patchEntity: ActionCreatorWithPayload<PatchActionPayload>;
    deleteEntity: ActionCreatorWithPayload<number>;
    setEditMode: ActionCreatorWithPayload<boolean>;
}

export function kCreateBaseStore<TEntity extends IReadModel>(
    sliceName: string,
    client: BaseModelRequest<TEntity>,
    selector: (state: any) => BaseState<TEntity>
) {

    const adapter = createEntityAdapter<TEntity>({
        selectId: (entity) => entity.id,
        sortComparer: compareByName,
    })

    const actions: BaseActions = {
        initializeStore: createAction<void>(`${sliceName}/initializeStore`),
        fetchEntities: createAction<object>(`${sliceName}/fetchEntities`),
        fetchEntity: createAction<number>(`${sliceName}/fetchEntity`),
        fetchEntitiesWithSetAll: createAction<object>(`${sliceName}/fetchEntitiesWithSetAll`),
        createEntity: createAction<CreateActionPayload>(`${sliceName}/createEntity`),
        patchEntity: createAction<PatchActionPayload>(`${sliceName}/patchEntity`),
        deleteEntity: createAction<number>(`${sliceName}/deleteEntity`),
        setEditMode: createAction<any>(`${sliceName}/setEditMode`),
    }

    const slice = createSlice({
        name: sliceName,
        initialState: adapter.getInitialState({
            isInitialized: false,
            isLoading: false,
            apiError: null,
            editMode: false,
            createdEntityId: null
        }) as BaseState<TEntity>,
        reducers: {
            // @ts-ignore
            upsertMany: adapter.upsertMany,
            // @ts-ignore
            setAll: adapter.setAll,
            // @ts-ignore
            upsertOne: adapter.upsertOne,
            // @ts-ignore
            removeOne: adapter.removeOne,
            // @ts-ignore
            removeAll: adapter.removeAll,
            setInitialized: (state, action) => {
                state.isInitialized = action.payload
            },
            setApiError: (state, action) => {
                state.apiError = action.payload
            },
            setEditMode: (state, action) => {
                state.editMode = action.payload;
            },
            setCreatedEntityId: (state, action: PayloadAction<string, number>) => {
                state.createdEntityId = action.payload;
            },
            setIsLoading: (state, action: PayloadAction<string, boolean>) => {
                state.isLoading = action.payload;
            }
        }
    });

    const adapterSelectors = adapter.getSelectors(selector);
    const selectors: BaseSelectors<TEntity> = {
        ...adapterSelectors,
        selectByIds: createSelector(
            adapterSelectors.selectEntities,
            (state: any, ids: number[]) => ids,
            (entities, ids: number[]) => ids.map(id => entities[id]!).filter(service => !!service)
        ),
        selectIsInitialized: createSelector(selector, store => store.isInitialized),
        selectApiError: createSelector(selector, store => store.apiError),
        selectEditMode: createSelector(selector, store => store.editMode),
        selectIsLoading: createSelector(selector, store => store.isLoading),
        selectCreatedEntity: createSelector(selector, store =>
            store.createdEntityId ? store.entities[store.createdEntityId] : undefined),
    }

    function* initializeStore(action: { type: string, payload: {} }) {
        const isInitialized: boolean = yield select(selectors.selectIsInitialized);
        if (isInitialized) return;
        yield put(actions.fetchEntities(action.payload))
    }

    function* fetchEntities(action: { type: string, payload: object }) {
        try {
            const result: ApiListResult<TEntity> = yield call(client.get, action.payload);
            yield put(slice.actions.upsertMany(result.results));
            yield put(slice.actions.setInitialized(true));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
            yield put(slice.actions.setInitialized(false));
        }
    }

    function* fetchEntity(action: { type: string, payload: number }) {
        yield put(slice.actions.setIsLoading(true));
        try {
            const entity: TEntity = yield call(client.detail, action.payload);
            yield put(slice.actions.upsertOne(entity));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
        }
        yield put(slice.actions.setIsLoading(false));
    }

    function* fetchEntitiesWithSetAll(action: { type: string, payload: object }) {
        yield put(slice.actions.setIsLoading(true));
        yield put(slice.actions.removeAll([]));
        try {
            const result: ApiListResult<TEntity> = yield call(client.get, action.payload);
            yield put(slice.actions.setAll(result.results));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
        }
        yield put(slice.actions.setIsLoading(false));
    }

    function* createEntity(action: { type: string, payload: CreateActionPayload }) {
        try {
            const entity: TEntity = yield call(client.post, action.payload.entity);
            yield put(slice.actions.upsertOne(entity));
            yield put(slice.actions.setApiError(null));
            yield put(slice.actions.setEditMode(false));
            yield put(slice.actions.setCreatedEntityId(entity.id));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
        }
    }

    function* patchEntity(action: { type: string, payload: PatchActionPayload }) {
        try {
            const entity: TEntity = yield call(client.patch, action.payload.id, action.payload.entity);
            yield put(slice.actions.upsertOne(entity));
            yield put(slice.actions.setApiError(null));
            yield put(slice.actions.setEditMode(false));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
        }
    }

    function* deleteEntity(action: { type: string, payload: number }) {
        try {
            yield call(client.delete, action.payload);
            yield put(slice.actions.removeOne(action.payload));
            yield put(slice.actions.setApiError(null));
            yield put(slice.actions.setEditMode(false));
        } catch (error) {
            yield put(slice.actions.setApiError(error));
        }
    }

    function* sagas() {
        yield takeEvery(actions.initializeStore.type, initializeStore);
        yield takeEvery(actions.fetchEntities.type, fetchEntities);
        yield takeEvery(actions.fetchEntity.type, fetchEntity);
        yield takeEvery(actions.fetchEntitiesWithSetAll.type, fetchEntitiesWithSetAll);
        yield takeEvery(actions.createEntity.type, createEntity);
        yield takeEvery(actions.patchEntity.type, patchEntity);
        yield takeEvery(actions.deleteEntity.type, deleteEntity);
    }

    return {
        actions,
        adapter,
        reducer: slice.reducer,
        slice,
        sagas,
        selectors
    }
}
