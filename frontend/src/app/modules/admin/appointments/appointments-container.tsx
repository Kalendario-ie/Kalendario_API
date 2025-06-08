import React from 'react';
import {Appointment} from 'src/app/api/appointments';
import SchedulingDateSelectorContainer from 'src/app/modules/admin/appointments/date-selector/scheduling-date-selector-container';
import TimeLineContainer from 'src/app/modules/admin/appointments/employee-panel/TimeLineContainer';
import AppointmentUpsertForm from 'src/app/modules/admin/appointments/forms/appointment-upsert-form';
import SchedulingPanelsSelector from 'src/app/modules/admin/appointments/scheduling-panels/scheduling-panels-selector';
import {useEditModal, useInitializeEffect} from 'src/app/shared/admin/hooks';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import {appointmentActions, appointmentSelectors} from 'src/app/store/admin/appointments';
import {employeeActions} from 'src/app/store/admin/employees';
import {scheduleActions} from 'src/app/store/admin/schedules';
import {
    EmployeePanelHeadersContainer,
    EmployeePanelsBodyContainer,
    useReloadAppointmentsEffect
} from './employee-panel';


const AppointmentsContainer: React.FunctionComponent = () => {
    useInitializeEffect(employeeActions);
    useInitializeEffect(scheduleActions);
    useReloadAppointmentsEffect();
    const [openModal, formModal] = useEditModal<Appointment>(appointmentSelectors, appointmentActions, AppointmentUpsertForm);

    return (
        <KFlexColumn>
            {formModal}
            <KFlexColumn className="sticky-top bg-white-gray">
                <KFlexRow>
                    <SchedulingPanelsSelector/>
                </KFlexRow>
                <KFlexRow>
                    <SchedulingDateSelectorContainer/>
                </KFlexRow>
                <EmployeePanelHeadersContainer onCreateClick={openModal}/>
            </KFlexColumn>
            <TimeLineContainer/>
            <EmployeePanelsBodyContainer onSelect={openModal}/>
        </KFlexColumn>
    )
}


export default AppointmentsContainer;
