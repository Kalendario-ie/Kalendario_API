import moment, {Moment} from 'moment';
import {RequestModel} from 'src/app/api/requests';
import {SlotDict} from 'src/app/store/companies/reducers';
import {RootState} from 'src/app/store/store';
import {CompanyDetails} from '../../api/companies';
import { createSelector } from '@reduxjs/toolkit';


export const selectOwnerId: (rootState: RootState) => number | null =
    (rootState) => rootState.companies.ownerId;


export const selectCompany: (rootState: RootState) => CompanyDetails | null =
    (rootState) => rootState.companies.company;


export const selectSlots: (rootState: RootState) => SlotDict =
    (rootState) => rootState.companies.slots;


export const selectSelectedSlotId: (rootState: RootState) => number | null =
    (rootState) => rootState.companies.selectedSlotId;



export const selectSelectedDate: (rootState: RootState) => Moment =
    (rootState) => moment.utc(rootState.companies.selectedDate);


export const selectCurrentRequest: (rootState: RootState) => RequestModel | null =
    (rootState) => rootState.companies.currentRequest;



export const selectSelectedServiceId: (rootState: RootState) => number | null =
    (rootState) => rootState.companies.selectedServiceId;


export const selectCompanyRequestCompleted: (rootState: RootState) => boolean =
    (rootState) => rootState.companies.companyRequestCompleted;


export const selectCurrentRequestCompleted: (rootState: RootState) => boolean =
    (rootState) => rootState.companies.currentRequestCompleted;


const selectServices = createSelector(
    [selectCompany],
    (company) =>
        company?.services
)


export const selectService = createSelector(
    [selectServices, selectSelectedServiceId],
    (services, id) =>
        services && services.find(service => service.id === id)
)

export const selectIsStoreReady = createSelector(
    [selectCompanyRequestCompleted, selectCurrentRequestCompleted],
    (company, request) => company && request

)

export const selectCartIsEmpty = createSelector(
    [selectCurrentRequest],
    (request) => !!request && request.itemsCount === 0
)

export const selectCartIsLoadedAndEmpty = createSelector(
    [selectCartIsEmpty, selectIsStoreReady],
    (emptyCart, storeReady) => storeReady && emptyCart
)
