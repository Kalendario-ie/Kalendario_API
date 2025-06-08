import moment from 'moment';

export const adminDashboard = 'adminDashboard';

export interface AdminDashboardState {
    currentDate: string;
    selectedPanelId: number | null,
    panelHours: number[];
    slotSize: number;
}

export const initialState: AdminDashboardState = {
    currentDate: moment.utc().startOf('day').toISOString(),
    selectedPanelId: null,
    panelHours: Array.from(Array(24).keys()),
    slotSize: 6
}
