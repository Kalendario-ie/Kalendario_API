import React from 'react';
import {KBaseInputProps} from 'src/app/shared/components/primitives/inputs/interfaces';

interface KColorInputProps extends KBaseInputProps {
    value: string;
    name: string;
}

export const KColorInput: React.FunctionComponent<KColorInputProps> = (
    {
        value,
        name,
        className,
        onBlur,
        onChange,
    }) => {
    return (
        <input
            className={className}
            name={name}
            onBlur={onBlur}
            type="color"
            onChange={onChange}
            value={value}/>
    )
}
