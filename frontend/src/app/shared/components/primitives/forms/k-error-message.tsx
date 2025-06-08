import React from 'react';
import {FormGroup} from 'reactstrap';

interface ErrorMessageProps {
    message: string | null | undefined;
}

export const KErrorMessage: React.FunctionComponent<ErrorMessageProps> = (
    {
        message
    }) => {
    return (
        <FormGroup>
            <div className="text-danger">{message}</div>
        </FormGroup>
    )
}
