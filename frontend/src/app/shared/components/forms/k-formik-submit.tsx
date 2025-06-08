import {useFormikContext} from 'formik';
import React from 'react';
import {KButton} from '../primitives';

export interface KFormikSubmitProps {
    text?: React.ReactNode;
    className?: string;
    isBlock?: boolean;
}

export const KFormikSubmit: React.FunctionComponent<KFormikSubmitProps> = (
    {
        text = 'Submit',
        className = '',
        isBlock = false
    }) => {
    const formik = useFormikContext();
    className += " btn-primary";
    if (isBlock) {
        className += ' btn-block';
    }
    return (
        <KButton
            color="primary"
            disabled={!formik.isValid}
            className={className}
            type="submit">{text}
        </KButton>
    )
}

