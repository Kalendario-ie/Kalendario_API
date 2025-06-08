import {ErrorMessage, useFormikContext} from 'formik';
import moment, {Moment} from 'moment';
import React from 'react';
import Datetime from 'react-datetime';
import {FormGroup} from 'reactstrap';
import {momentToIso, stringToMoment} from 'src/app/shared/util/moment-helpers';

interface KDatetimeInput {
    name: string
}

const KFormikDatetimeInput: React.FunctionComponent<KDatetimeInput> = (
    {
        name,
    }) => {
    const formik = useFormikContext();
    const fieldMeta = formik.getFieldMeta(name);
    const fieldHelpers = formik.getFieldHelpers(name);

    const handleDateChange = (e: Moment | string) => {
        fieldHelpers.setValue(moment.isMoment(e) ? momentToIso(e) : e);
    }

    return (
        <FormGroup>
            <Datetime
                closeOnClickOutside={true}
                inputProps={{
                    readOnly: true,
                    name: name,
                    className: `form-control${(fieldMeta.error) ? ' is-invalid' : ''}`,
                }}
                initialValue={stringToMoment(formik.getFieldProps(name).value)}
                onChange={handleDateChange}
            />
            <ErrorMessage name={name}/>
        </FormGroup>
    )
}


export default KFormikDatetimeInput;
