import React from 'react';
import {Input, Label} from 'reactstrap';
import {KBaseInputProps} from 'src/app/shared/components/primitives/inputs/interfaces';

interface KCheckboxProps extends KBaseInputProps {
}

export const KCheckbox: React.FunctionComponent<KCheckboxProps> = (
    {
        placeholder,
        name,
        checked,
        value,
        onChange,
        onBlur
    }) => {
    return (
        <Label check>
            <Input type="checkbox"
                   name={name}
                   onChange={onChange}
                   onBlur={onBlur}
                   checked={checked || !!value}
            />
            {placeholder}
        </Label>
    )
}
