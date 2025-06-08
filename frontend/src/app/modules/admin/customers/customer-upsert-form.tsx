import React from 'react';
import {Customer, saveCustomerRequestParser} from 'src/app/api/customers';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import * as yup from 'yup';

const CustomerUpsertForm: React.FunctionComponent<AdminEditContainerProps<Customer>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const validation = yup.object().shape({
        firstName: yup.string().required(),
        lastName: yup.string().required(),
        email: yup.string().required().email(),
    });

    return (
        <KFormikForm initialValues={saveCustomerRequestParser(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={validation}
        >
            <KFormikInput name="firstName"/>
            <KFormikInput name="lastName"/>
            <KFormikInput name="email"/>
            <KFormikInput name="phone"/>
            <KFormikInput as="textarea" name="warning"/>
        </KFormikForm>
    )
}


export default CustomerUpsertForm;
