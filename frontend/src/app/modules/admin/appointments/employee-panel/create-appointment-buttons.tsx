import {Moment} from 'moment';
import React from 'react';
import {Appointment, blankCustomerAppointment, blankEmployeeEvent} from 'src/app/api/appointments';
import {Employee} from 'src/app/api/employees';
import {KIconButton} from 'src/app/shared/components/primitives/buttons';

interface CreateAppointmentButtonsProps {
    employee: Employee;
    onCreateClick: (entity: Appointment | null) => () => void;
    currentDate: Moment;
    hour: number;
    minute: number;
}

const CreateAppointmentButtons: React.FunctionComponent<CreateAppointmentButtonsProps> = (
    {
        employee,
        onCreateClick,
        currentDate,
        hour,
        minute
    }) => {
    const employeeId = employee.id;
    const selectedTime = () => currentDate.clone().add(hour, 'hour').add(minute, 'minute');
    const handleAddClick = () =>
        onCreateClick(blankCustomerAppointment(employeeId, selectedTime()))();
    const handleLockClick = () =>
        onCreateClick(blankEmployeeEvent(employeeId, selectedTime().add(minute, 'minute')))();

    return (
        <>
            <KIconButton color="primary" icon={'plus'} onClick={handleAddClick}/>
            <KIconButton color="accent" icon={'lock'} onClick={handleLockClick}/>
        </>
    )
}


export default CreateAppointmentButtons;
