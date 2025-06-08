import moment, {Moment} from 'moment';
import React, {useEffect} from 'react';
import {Button} from 'reactstrap';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import {KIconButton} from 'src/app/shared/components/primitives/buttons';
import {KDateInput} from 'src/app/shared/components/primitives/inputs';
import {momentToIso} from 'src/app/shared/util/moment-helpers';
import {useKHistory, useQueryParams} from 'src/app/shared/util/router-extensions';
import {useAppDispatch, useAppSelector} from 'src/app/store';
import {adminDashboardActions, adminDashboardSelectors} from 'src/app/store/admin/dashboard';

interface SchedulingDateSelectorProps {
    date: Moment;
    dateChange: (date: Moment) => void;
}
const SchedulingDateSelector: React.FunctionComponent<SchedulingDateSelectorProps> = ({date, dateChange}) => {

    const handleNextClick = () => {
        dateChange(date.clone().add(1, 'day'))
    }
    const handleTodayClick = () => {
        dateChange(moment.utc().startOf('day'));
    }

    const handlePreviousClick = () => {
        dateChange(date.clone().subtract(1, 'day'))
    }

    return (
        <KFlexRow className="sticky-top-left p-2" align={'center'}>
            <Button color="primary" size="sm" onClick={handleTodayClick}>Today</Button>
            <KIconButton icon="chevron-left" color="accent" onClick={handlePreviousClick}/>
            <KIconButton icon="chevron-right" color="accent" onClick={handleNextClick}/>
            {date.format('dddd')}
            <KFlexColumn align="center" className="ml-2">
                <KDateInput value={date} onChange={dateChange}/>
            </KFlexColumn>
        </KFlexRow>
    )
}

const SchedulingDateSelectorContainer: React.FunctionComponent = () => {
    const currentDate = useAppSelector(adminDashboardSelectors.selectCurrentDate);
    const dispatch = useAppDispatch();
    const params = useQueryParams();
    const history = useKHistory();

    useEffect(() => {
        let date = (params['date'] || currentDate);
        dispatch(adminDashboardActions.setCurrentDate(moment.utc(date).startOf('day')));
    }, [currentDate, dispatch, params]);

    const handleDateChange = (date: Moment) => {
        history.push(history.location.pathname, {...params, date: momentToIso(date)})
    }

    return (
        <SchedulingDateSelector date={currentDate}
                                dateChange={handleDateChange}
        />
    )
}


export default SchedulingDateSelectorContainer;
