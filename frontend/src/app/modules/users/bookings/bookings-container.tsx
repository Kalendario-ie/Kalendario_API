import moment from 'moment'
import React, {useEffect} from 'react';
import {Calendar, momentLocalizer, stringOrDate} from 'react-big-calendar'
import {useDispatch, useSelector} from 'react-redux';
import {Appointment} from 'src/app/api/appointments';
import {RequestModelGetParams} from 'src/app/api/companies';
import EventModal from 'src/app/modules/users/bookings/event-modal';
import {KCard, KPageContainer} from 'src/app/shared/components/primitives/containers';
import {stringToMoment, validOrToday} from 'src/app/shared/util/moment-helpers';
import {useQueryParams} from 'src/app/shared/util/router-extensions';
import {eventsRequest, selectEvents, selectSelectedEvent, setSelectedEvent} from 'src/app/store/users';


const BookingsContainer: React.FunctionComponent = () => {
    const events = useSelector(selectEvents)
        ?.map(a => ({...a, title: a.companyName}));
    const selectedEvent = useSelector(selectSelectedEvent);
    const dispatch = useDispatch();
    const {date} = useQueryParams();

    const initialDate = validOrToday(date);

    useEffect(() => {
        dispatch(eventsRequest({start: initialDate.clone().startOf('month'), end: initialDate.clone().endOf('month')}))
    }, [dispatch, initialDate]);


    const updateEvents = (range: Date[] | { start: stringOrDate; end: stringOrDate }) => {
        const request: RequestModelGetParams = Array.isArray(range)
            ? {start: stringToMoment(range[0]), end: stringToMoment(range[range.length - 1])}
            : {start: stringToMoment(range.start), end: stringToMoment(range.end)}
        dispatch(eventsRequest(request));
    }

    const selectEvent = (appointment: Appointment) => dispatch(setSelectedEvent(appointment))
    const closeModal = () => dispatch(setSelectedEvent(null));

    return (
        <KPageContainer>
            <KCard>
                <Calendar
                    date={initialDate.toDate()}
                    localizer={momentLocalizer(moment)}
                    events={events || []}
                    startAccessor="start"
                    endAccessor="end"
                    style={{height: 500}}
                    onRangeChange={updateEvents}
                    onSelectEvent={selectEvent}
                />
            </KCard>
            <EventModal appointment={selectedEvent}
                        closeClick={closeModal}/>
        </KPageContainer>
    )
}


export default BookingsContainer;
