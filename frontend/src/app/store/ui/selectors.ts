import { RootState } from "../store"


export const selectShowDashboardToggle: (rootState: RootState) => boolean =
    (rootState) => rootState.ui.showDashboardToggle

export const selectSidenavOpen: (rootState: RootState) => boolean =
    (rootState) => rootState.ui.sidenavOpen
