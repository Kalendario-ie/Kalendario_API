import {useFormikContext} from 'formik';
import React, {useState} from 'react';
import {FormattedMessage} from 'react-intl';
import {timeFromString, timeToString} from 'src/app/api/common/models';
import {UpsertScheduleRequestFrame} from 'src/app/api/schedule/requests';
import {KFlexColumn} from 'src/app/shared/components/flex';
import {KFormikInput} from 'src/app/shared/components/forms';
import KModal from 'src/app/shared/components/modal/k-modal';
import {KIconButton} from 'src/app/shared/components/primitives/buttons';
import KShowOnHoverContainer from 'src/app/shared/components/primitives/containers/k-show-on-hover-container';
import styles from './schedule-formik-input.module.scss';

interface ScheduleFrameProps {
    frame: UpsertScheduleRequestFrame;
    onClick: () => void;
}

const ScheduleFrame: React.FunctionComponent<ScheduleFrameProps> = (
    {
        frame,
        onClick
    }) => {
    const [start, end] = [timeFromString(frame.start), timeFromString(frame.end)];
    const top = +(start.hour + 1 + start.minute / 60) * 3
    const height = ((end.hour + end.minute / 60) - (start.hour + start.minute / 60)) * 3

    return (
        <div className={`${styles.frameBox} bg-accent c-pointer`}
             onClick={onClick}
             style={{
                 top: `${top}rem`,
                 height: `${height}rem`
             }}/>
    )
}

interface ScheduleFormikInputProps {
    name: string;

}

const ScheduleFormikInput: React.FunctionComponent<ScheduleFormikInputProps> = (
    {
        name
    }) => {
    const formik = useFormikContext();
    const accessor = `${name}.frames`;
    const formikValues = formik.getFieldProps<UpsertScheduleRequestFrame[]>(accessor);
    const formikHelpers = formik.getFieldHelpers(accessor);
    const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const isMonday = name === 'mon';
    const hours = Array.from(Array(24).keys());
    const className = `${styles.lineCell} ${isMonday ? '' : styles.borderLeft}`;

    const handleAddClick = (hour: number) => () => {
        const newFrame = {start: timeToString({hour, minute: 0}), end: timeToString({hour: hour + 1, minute: 0})};
        const values = [...formikValues.value, newFrame];
        formikHelpers.setValue(values);
        setSelectedIndex(values.length - 1);
        setIsModalOpen(true);
    }

    const handleFrameClick = (index: number) => () => {
        setSelectedIndex(index);
        setIsModalOpen(true);
    }

    const handleModalCancel = () => {
        setIsModalOpen(false);
        setSelectedIndex(null);
    }

    const handleModalDelete = () => {
        const toDelete = selectedIndex!;
        setIsModalOpen(false);
        setSelectedIndex(null);
        formikValues.value.splice(toDelete, 1);
    }

    const hourCell = (hour: number) =>
        <KFlexColumn className="position-relative">
            {isMonday && <div className={styles.hourBox}>{timeToString({hour, minute: 0})}</div>}
            <KShowOnHoverContainer className={className}>
                <KIconButton color="primary" onClick={handleAddClick(hour)} icon="plus-square"/>
            </KShowOnHoverContainer>
        </KFlexColumn>

    const modal = <KModal header={<FormattedMessage id="ADMIN.SCHEDULE.EDIT-FRAME-MODAL"/>}
                          body={
                              <>
                                  {accessor &&
                                  <>
                                      <KFormikInput placeholder="Start"
                                                    name={`${accessor}[${selectedIndex}].start`}
                                                    type="time"/>
                                      <KFormikInput placeholder="End"
                                                    name={`${accessor}[${selectedIndex}].end`}
                                                    type="time"/>
                                  </>
                                  }
                              </>
                          }
                          onCancel={handleModalCancel}
                          isOpen={isModalOpen}
                          buttons={[
                              {text: 'confirm', onClick: handleModalCancel, color: 'primary'},
                              {text: 'delete', onClick: handleModalDelete, color: 'danger'}
                          ]}
    />

    return (
        <>
            <KFlexColumn className="position-relative" align={'center'}>
                <div className={className}>{name}</div>
                {formikValues.value.map((frame, i) =>
                    <ScheduleFrame key={i}
                                   frame={frame}
                                   onClick={handleFrameClick(i)}/>
                )}
                {hours.map((hour, i) => hourCell(hour))}
            </KFlexColumn>
            {modal}

        </>

    )
}


export default ScheduleFormikInput;
