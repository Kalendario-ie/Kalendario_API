import {Formik} from 'formik';
import {FormikHelpers, FormikProps} from 'formik/dist/types';
import React, {useEffect, useState} from 'react';
import {Form, FormGroup} from 'reactstrap';
import {ApiValidationError} from 'src/app/api/common/api-errors';
import KFormikErrorHandler from 'src/app/shared/components/forms/k-formik-error-handler';
import KFormikStandardButtons from 'src/app/shared/components/forms/k-formik-standard-buttons';

export interface KFormikFormProps<Values> {
    initialValues: Values;
    apiError: ApiValidationError | null;
    validationSchema?: any | (() => any);
    onSubmit: (values: Values, formikHelpers: FormikHelpers<Values>) => void;
    onCancel?: () => void;
    children: ((props: FormikProps<Values>) => React.ReactNode) | React.ReactNode;
    errors?: string[];
}

export function KFormikForm<Values>(
    {
        initialValues,
        apiError,
        onSubmit,
        onCancel,
        children,
        validationSchema
    }: KFormikFormProps<Values>) {
    const [errors, setErrors] = useState<string[]>([]);
    useEffect(() => {
        if (apiError?.detail && apiError.detail['nonFieldErrors']) {
            setErrors(apiError.detail['nonFieldErrors']);
        }
    }, [apiError]);

    return (
        <Formik initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={onSubmit}>
            {(formik) => (
                <Form className="is-invalid" onSubmit={(e) => {
                    e.preventDefault();
                    formik.handleSubmit(e);
                }}>
                    <FormGroup className="text-danger">
                        {errors.map((error, key) => <div key={key}>{error}</div>)}
                    </FormGroup>
                    <KFormikErrorHandler apiError={apiError}/>

                    {typeof children == 'function'
                        ? (children as (props: FormikProps<Values>) => React.ReactNode)(formik)
                        : children}

                    {onCancel &&
                    <KFormikStandardButtons onCancel={onCancel}/>
                    }
                </Form>
            )}
        </Formik>
    )
}

