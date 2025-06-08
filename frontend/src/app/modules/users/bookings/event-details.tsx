import React from 'react';
import {CustomerRequestAppointment} from 'src/app/api/appointments';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';
import KIcon from 'src/app/shared/components/primitives/k-icon';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';

interface EventDetailsProps {
    appointment: CustomerRequestAppointment;
}

const EventDetails: React.FunctionComponent<EventDetailsProps> = (
    {
        appointment
    }) => {
    return (
        <KFlexRow className="flex-fill" align={'center'}>
            <AvatarImg size={4} src={appointment.employee.photoUrl}/>
            <KFlexColumn className="pl-2 flex-fill">
                <KFlexRow justify={'between'}>
                        <span>
                        <KIcon icon="calendar"/>
                            {stringToMoment(appointment.start).format('DD - MMMM')}
                        </span>
                    <span>
                        <KIcon icon="clock-o"/>
                        {stringToMoment(appointment.start).format('HH:mm - ')}
                        {stringToMoment(appointment.end).format('HH:mm')}
                        </span>
                </KFlexRow>
                <div>
                    {appointment.employee.name}
                </div>
                <KFlexRow>
                    {appointment.service.name}
                    <span className="flex-fill c-primary text-right">
                        {appointment.service.price}
                        </span>
                </KFlexRow>
            </KFlexColumn>
        </KFlexRow>

    )
}


export default EventDetails;
