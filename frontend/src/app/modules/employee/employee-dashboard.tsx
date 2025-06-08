import moment, {Moment} from 'moment';
import React, {useEffect, useState} from 'react';
import {isMobile} from 'react-device-detect';
import {useSelector} from 'react-redux';
import {adminAppointmentClient, Appointment} from 'src/app/api/appointments';
import {getShift, Schedule} from 'src/app/api/schedule';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import {KIconButton, KRoundedButton} from 'src/app/shared/components/primitives/buttons';
import {KCard} from 'src/app/shared/components/primitives/containers';
import KIcon from 'src/app/shared/components/primitives/k-icon';
import {momentToIso, stringToMoment} from 'src/app/shared/util/moment-helpers';
import {selectUserEmployee} from 'src/app/store/auth';

function dates(startDate: Moment, endDate: Moment): Moment[] {
    const dates = [];
    let controlDate = moment.utc(startDate.toISOString());
    while (controlDate.isBefore(endDate) || controlDate.isSame(endDate)) {
        dates.push(moment.utc(controlDate.toISOString()));
        controlDate = controlDate.clone().add(1, 'day');
    }
    return dates;
}

interface EmployeeDashboardDatePickerProps {
    currentDate: Moment;
    dateChange: (date: Moment) => void;
}

const EmployeeDashboardDatePicker: React.FunctionComponent<EmployeeDashboardDatePickerProps> = ({
                                                                                                    currentDate,
                                                                                                    dateChange
                                                                                                }) => {
    const timeSpan = isMobile ? 2 : 3;
    const [startDate, setStartDate] = useState(currentDate.clone().startOf('day').subtract(timeSpan, 'day'));
    const [endDate, setEndDate] = useState(currentDate.clone().startOf('day').add(timeSpan, 'day'));
    const week = dates(startDate, endDate);

    const updateDates = (date: Moment) => {
        dateChange(date);
        if (date > endDate) {
            setStartDate(date.clone());
            setEndDate(date.clone().add(timeSpan * 2, 'day'));
        }
        if (date < startDate) {
            setStartDate(date.clone().subtract(timeSpan * 2, 'day'));
            setEndDate(date.clone());
        }
    }

    const previousClick = () => {
        updateDates(currentDate.clone().subtract(1, 'day'))
    }

    const nextClick = () => {
        updateDates(currentDate.clone().add(1, 'day'))
    }

    return (
        <>
            <KFlexRow justify="between" className="mb-2">
                <KIconButton icon="chevron-left" color="primary" onClick={previousClick}/>
                {currentDate.format('MMMM YYYY').toUpperCase()}
                <KIconButton icon="chevron-right" color="primary" onClick={nextClick}/>
            </KFlexRow>
            <KFlexRow justify="between" className="mb-2">
                {week.map((day, index) =>
                    <KFlexColumn key={index} className="m-2" align="center" justify="center">
                        {day.format('ddd').toUpperCase()}
                        <KRoundedButton
                            className="mt-2"
                            color={`${day.date() === currentDate.date() ? 'accent' : 'primary'}`}
                            onClick={() => updateDates(day.clone())}
                        >
                            {day.date()}
                        </KRoundedButton>
                    </KFlexColumn>
                )}
            </KFlexRow>
            <div>
                <hr/>
            </div>
            <KFlexRow justify="center" align="center">
                <KIcon icon="calendar" margin={2}/>
                {currentDate.format('dddd, DD MMM YY')}
            </KFlexRow>
        </>
    )
}

interface EmployeeScheduleViewProps {
    date: Moment;
    schedule: Schedule;
}

const EmployeeScheduleView: React.FunctionComponent<EmployeeScheduleViewProps> = ({date, schedule}) => {
    const shift = getShift(schedule, date);
    return (
        <KFlexRow justify="center">
            {shift && shift.frames.map((frame, index) =>
                <React.Fragment key={index}>
                    {index !== 0 ? ' |' : ''} {frame.name}
                </React.Fragment>
            )}
            {!shift &&
            <>
                No shift available
            </>
            }
        </KFlexRow>
    )
}

interface EmployeeDashboardAppointmentsProps {
    appointment: Appointment;
}

const EmployeeDashboardAppointment: React.FunctionComponent<EmployeeDashboardAppointmentsProps> = ({appointment}) => {
    const start = stringToMoment(appointment.start).format('HH:mm')
    const end = stringToMoment(appointment.end).format('HH:mm')

    const customerNotes = 'customerNotes' in appointment ? appointment.customerNotes : '';
    const customerName = 'customer' in appointment ? appointment.customer?.name : '';
    const serviceName = 'service' in appointment ? appointment.service?.name : '';

    return (
        <KFlexColumn key={appointment.id}>
            <KFlexRow className="font-weight-bolder mb-2" justify="center">
                {serviceName}
            </KFlexRow>
            <KFlexRow align="center" className="mb-2">
                <KIcon icon="clock" color="primary" margin={2}/> {`${start} - ${end}`}
            </KFlexRow>
            {customerName &&
            <KFlexRow align="center" className="mb-2">
                <KIcon icon="address-card" color="primary" margin={2}/> {customerName}
            </KFlexRow>
            }
            {appointment.internalNotes &&
            <KFlexRow align="center" className="mb-2">
                <KIcon icon="sticky-note" color="primary" margin={2}/> {appointment.internalNotes}
            </KFlexRow>
            }
            {customerNotes &&
            <KFlexRow align="center" className="mb-2">
                <KIcon icon="comment-alt" color="primary" margin={2}/> {customerNotes}
            </KFlexRow>
            }
        </KFlexColumn>
    )
}

const EmployeeDashboard: React.FunctionComponent = () => {
    const [currentDate, setCurrentDate] = useState(moment.utc());
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const employee = useSelector(selectUserEmployee);

    useEffect(() => {
        adminAppointmentClient.get(
            {
                employee: employee?.id,
                from_date: momentToIso(currentDate.clone().startOf('day')),
                to_date: momentToIso(currentDate.clone().endOf('day')),
            }).then(res => setAppointments(res.results));
    }, [currentDate, employee?.id]);


    return (
        <KFlexColumn className="h-100vh pt-2" align="center" justify="center">
            {employee &&
            <KCard className="h-100" maxWidth={600} hasShadow={!isMobile} hasBorder={!isMobile}>
                <KFlexColumn className="h-100">
                    <KFlexRow justify="center" className="mb-3">
                        {employee.name}
                    </KFlexRow>
                    <EmployeeDashboardDatePicker currentDate={currentDate} dateChange={setCurrentDate}/>
                    <div>
                        <hr/>
                    </div>
                    <EmployeeScheduleView schedule={employee.schedule} date={currentDate}/>
                    <div>
                        <hr/>
                    </div>
                    <div className="flex-fill overflow-auto">
                        {appointments.map(appointment => <React.Fragment key={appointment.id}>
                                <EmployeeDashboardAppointment appointment={appointment}/>
                                <hr/>
                            </React.Fragment>
                        )}
                    </div>
                </KFlexColumn>
            </KCard>
            }
        </KFlexColumn>
    )
}


export default EmployeeDashboard;
