import {PermissionModel} from 'src/app/api/auth';
import {SchedulingPanel} from 'src/app/api/scheduling-panels/models';
import {UpsertSchedulingPanelRequest} from 'src/app/api/scheduling-panels/requests';


export function schedulingPanelParser(data: any): SchedulingPanel {
    return {
        ...data,
        permissionModel: PermissionModel.schedulingpanel,
    }
}

export function upsertSchedulingPanelRequestParser(panel: SchedulingPanel | null): UpsertSchedulingPanelRequest {
    return panel ? {name: panel.name, employees: panel.employees} : {employees: [], name: ''}
}
