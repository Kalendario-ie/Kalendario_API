import {useFormikContext} from 'formik';
import React, {useEffect} from 'react';
import {ApiValidationError} from 'src/app/api/common/api-errors';

interface KFormikErrorHandlerProps {
    apiError: ApiValidationError | null;
}

const KFormikErrorHandler: React.FunctionComponent<KFormikErrorHandlerProps> = (
    {
        apiError,
    }) => {
    const formik = useFormikContext();
    useEffect(() => {
        if (apiError?.detail) {
            Object.keys(apiError.detail).forEach(key => {
                if (key !== 'nonFieldErrors' && Array.isArray(apiError.detail[key])) {
                    const error = apiError.detail[key].reduce(((previousValue, currentValue) => previousValue + currentValue), '');
                    formik.setFieldError(key,  error);
                }
            })
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [apiError]);


    return (
        <></>
    )
}


export default KFormikErrorHandler;
