import React from 'react';
import {PermissionModel} from 'src/app/api/auth';
import SchedulesTable from 'src/app/modules/admin/schedules/schedules-table';
import ScheduleUpsertForm from 'src/app/modules/admin/schedules/schedule-upsert-form';
import AdminListEditContainer from 'src/app/shared/admin/admin-list-edit-container';
import {scheduleActions, scheduleSelectors} from 'src/app/store/admin/schedules';


interface SchedulesContainerProps {
}

const SchedulesContainer: React.FunctionComponent<SchedulesContainerProps> = () => {
    return (
            <AdminListEditContainer baseSelectors={scheduleSelectors}
                                    baseActions={scheduleActions}
                                    modelType={PermissionModel.schedule}
                                    EditContainer={ScheduleUpsertForm}
                                    ListContainer={SchedulesTable}/>
    )
}


export default SchedulesContainer;
