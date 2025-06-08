import moment, {Moment} from 'moment';
import React from 'react';
import {Input} from 'reactstrap';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';

interface KDateInputProps {
    value?: Moment | string;
    onChange?: (value: Moment) => void;
}

export const KDateInput: React.FunctionComponent<KDateInputProps> = (
    {
        value,
        onChange
    }) => {
    const useValue = value && moment.isMoment(value) ? value : stringToMoment(value);
    return (
        <Input type='date'
               value={useValue && useValue.format('YYYY-MM-DD')}
               onChange={event => onChange && onChange(moment.utc(event.target.value))}/>
    )
}
