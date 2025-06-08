import {useFormikContext} from 'formik';
import moment, {Moment} from 'moment';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {FormGroup, Input, Label} from 'reactstrap';
import {CustomerAppointment} from 'src/app/api/appointments';
import {timeToString} from 'src/app/api/common/models';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import {KFormikCustomerInput, KFormikInput} from 'src/app/shared/components/forms';
import {KDateInput} from 'src/app/shared/components/primitives/inputs';
import {compareByName} from 'src/app/shared/util/comparers';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';
import {useAppSelector} from 'src/app/store';
import {employeeSelectors} from 'src/app/store/admin/employees';
import {serviceSelectors} from 'src/app/store/admin/services';

function addHours(date: Moment, time: string): string {
    const momentTime = moment.utc(time, 'HH:mm')
    return date.clone()
        .add(momentTime.hour(), 'hour')
        .add(momentTime.minutes(), 'minutes')
        .toISOString();
}

function useDateHelper(name: string): [Moment, (value: Moment) => void, string, (event: ChangeEvent<HTMLInputElement>) => void] {
    const formik = useFormikContext();
    const {value} = formik.getFieldMeta<string>(name);
    const {setValue} = formik.getFieldHelpers(name);

    const momentValue = stringToMoment(value);
    const [time, setTime] = useState(momentValue.format('HH:mm'));

    useEffect(() => {
        const momentValue = stringToMoment(value);
        setTime(momentValue.format('HH:mm'))
    }, [value]);

    const handleDateChange = (value: Moment) => {
        setValue((addHours(value.startOf('day'), time)));

    }
    const handleTimeChange = (e: ChangeEvent<HTMLInputElement>) => {
        setTime(e.target.value);
        setValue((addHours(momentValue.startOf('day'), e.target.value)));

    }


    return [momentValue, handleDateChange, time, handleTimeChange]
}

const FormikStartEndTimeInput: React.FunctionComponent = () => {
    const [start, handleDateChange, startTime, handleStartTimeChange] = useDateHelper('start');
    const [, handleEndDateChange, endTime, handleEndTimeChange] = useDateHelper('end');

    return (
        <>
            <FormGroup>
                <KFlexColumn>
                    <Label>Date</Label>
                    <KDateInput value={start}
                                onChange={(e) => {
                                    handleDateChange(e);
                                    handleEndDateChange(e);
                                }}/>
                </KFlexColumn>
            </FormGroup>
            <FormGroup>
                <KFlexRow align={'center'} justify={'center'}>
                    <KFlexColumn className="w-100">
                        Start
                        <Input value={startTime} onChange={handleStartTimeChange} type={'time'}/>
                    </KFlexColumn>
                    <KFlexColumn className="w-100">
                        Finish
                        <Input value={endTime} onChange={handleEndTimeChange} type={'time'}/>
                    </KFlexColumn>
                </KFlexRow>
            </FormGroup>
        </>
    )
}


function useEmployeeServices() {
    const formik = useFormikContext();
    const employeeId = formik.getFieldProps<number>('employee').value;
    const [employeeServices, setEmployeeServices] = useState<number[]>([]);
    const employeeEntities = useAppSelector(employeeSelectors.selectEntities);

    useEffect(() => {
        setEmployeeServices(employeeEntities[employeeId]?.services || [])
    }, [employeeEntities, employeeId]);

    return useAppSelector((state) => serviceSelectors
        .selectByIds(state, employeeServices))
        .sort(compareByName);
}

function useUpdateEndTimeOnServiceChangeEffect() {
    const formik = useFormikContext();
    const serviceId = formik.getFieldProps<number>('service').value;
    const start = formik.getFieldProps('start').value;
    const {setValue} = formik.getFieldHelpers('end');

    const [initialId, setInitialId] = useState(serviceId);
    const [initialStart, setInitialStart] = useState(start);

    const service = useAppSelector((state) => serviceSelectors.selectById(state, serviceId));

    useEffect(() => {
        if (service && (serviceId !== initialId || start !== initialStart)) {
            setInitialId(serviceId);
            setInitialStart(start);
            setValue(addHours(stringToMoment(start), timeToString(service.duration)))
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [initialId, start, service, serviceId, initialStart]);
}

interface CustomerAppointmentUpsertFormProps {
    appointment: CustomerAppointment | null;
}

const CustomerAppointmentUpsertForm: React.FunctionComponent<CustomerAppointmentUpsertFormProps> = ({appointment}) => {
    const employees = useAppSelector(employeeSelectors.selectAll);
    const services = useEmployeeServices();
    useUpdateEndTimeOnServiceChangeEffect();

    return (
        <>
            <FormikStartEndTimeInput/>
            <KFormikInput name="employee" as={'select'} options={employees}/>
            <KFormikInput name="service" as={'select'} options={services}/>
            <KFormikCustomerInput initialCustomer={appointment?.customer || null}/>
            <KFormikInput name="internalNotes" as={'textarea'}/>
            <KFormikInput placeholder="Allow Overlapping" name="ignoreAvailability" as={'checkbox'}/>
        </>
    )
}


export default CustomerAppointmentUpsertForm;
