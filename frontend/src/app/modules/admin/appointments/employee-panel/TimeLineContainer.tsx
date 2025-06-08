import React from 'react';
import {useSelector} from 'react-redux';
import {useHoursConverter} from 'src/app/modules/admin/appointments/employee-panel/hooks';
import {momentIsToday, momentToday} from 'src/app/shared/util/moment-helpers';
import {adminDashboardSelectors} from 'src/app/store/admin/dashboard';
import styles from './employee-panel.module.scss';


const TimeLineContainer: React.FunctionComponent = () => {
    const currentDate = useSelector(adminDashboardSelectors.selectCurrentDate);
    const isToday = momentIsToday(currentDate)
    const today = momentToday();
    const style: React.CSSProperties = {
        top: useHoursConverter(today)
    }

    return (
        <div className="position-relative">
            {isToday &&
            <div style={style} className={styles.currentTimeLine}/>
            }
        </div>
    )
}


export default TimeLineContainer;
