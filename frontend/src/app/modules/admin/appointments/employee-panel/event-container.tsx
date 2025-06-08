import moment, {Moment} from 'moment';
import React from 'react';
import {Spinner} from 'reactstrap';
import {Appointment, BaseAppointment, CustomerAppointment} from 'src/app/api/appointments';
import {Employee} from 'src/app/api/employees';
import styles from 'src/app/modules/admin/appointments/employee-panel/employee-panel.module.scss';
import {useHoursConverter} from 'src/app/modules/admin/appointments/employee-panel/hooks';
import {compareByStartDate} from 'src/app/shared/util/comparers';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';
import {useAppSelector} from 'src/app/store';
import {appointmentSelectors} from 'src/app/store/admin/appointments';
import {adminDashboardSelectors} from 'src/app/store/admin/dashboard';

interface EventProps {
    order: number;
    isOverlapping: boolean;
    appointment: Appointment;
    onClick: () => void;
    currentDate: Moment;
}

const BASE_WIDTH = 12.5;

const Event: React.FunctionComponent<EventProps> = (
    {
        order,
        isOverlapping,
        appointment,
        onClick,
        currentDate
    }) => {
    const start = moment.utc(appointment.start);
    const end = moment.utc(appointment.end);

    const isStartBeforeCurrentDate = React.useMemo(() =>
            start.clone().startOf('day') < currentDate.clone().startOf('day'),
        [start, currentDate]);

    const isEndAfterCurrentDate = React.useMemo(() =>
            end.clone().startOf('day') > currentDate.clone().startOf('day'),
        [end, currentDate]);

    const startTop = useHoursConverter(start);

    const customerAppointment = 'customer' in appointment && appointment.customer ? appointment as CustomerAppointment : null;


    const duration =
        isStartBeforeCurrentDate ?
            moment.duration(end.format('HH:mm')) :
            isEndAfterCurrentDate ?
                moment.duration(start.clone().endOf('day').diff(start)) :
                moment.duration(end.diff(start));

    const backgroundColor = customerAppointment ? customerAppointment.service.color : '#FFFFFF';
    const title = customerAppointment ? customerAppointment.customer.name : appointment.internalNotes;
    const subTitle = customerAppointment ? customerAppointment.service.name : '';

    const style: React.CSSProperties = {
        width: `${BASE_WIDTH - 0.25 - 3 * +isOverlapping}rem`,
        marginRight: '0.125rem',
        marginLeft: `${0.125 + 3 * +isOverlapping}rem`,
        zIndex: order + 2,
        top: isStartBeforeCurrentDate ? '0' : startTop,
        height: useHoursConverter(duration),
        backgroundColor,
    }

    return (
        <div style={style}
             className={`${styles.panelEvent} k-shadow-0`}
             onClick={onClick}
        >
            <div>
                {title}
            </div>
            {subTitle}
        </div>
    )
}

interface EventsContainerProps {
    employee: Employee;
    onSelect: (entity: Appointment | null) => () => void
}

const EventsContainer: React.FunctionComponent<EventsContainerProps> = (
    {
        employee,
        onSelect
    }) => {
    const appointments = useAppSelector(appointmentSelectors.selectAll);
    const isLoading = useAppSelector(appointmentSelectors.selectIsLoading);
    const currentDate = useAppSelector(adminDashboardSelectors.selectCurrentDate);

    const employeeAppointments = React.useMemo(() =>
            appointments
                .filter(appointment => appointment.employee.id === employee.id)
                .sort(compareByStartDate)
        , [appointments, employee.id]
    )

    return (
        <div className="position-relative">
            {isLoading &&
            <Spinner className="position-absolute"/>
            }
            {employeeAppointments.map((appointment, index) =>
                <Event key={appointment.id}
                       isOverlapping={index > 0 ? isOverlapping(appointment, employeeAppointments[index - 1]) : false}
                       order={index}
                       appointment={appointment}
                       onClick={onSelect(appointment)}
                       currentDate={currentDate}
                />
            )}
        </div>
    )
}

const isOverlapping = (currentAppointment: BaseAppointment, previousAppointment: BaseAppointment): boolean => {
    return stringToMoment(currentAppointment.start).isBefore(stringToMoment(previousAppointment.end));
}

export default EventsContainer;
