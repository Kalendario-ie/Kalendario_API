import React from 'react';
import {
    createUpsertServiceCategoryRequest,
    ServiceCategory,
    UpsertServiceCategoryRequestValidation
} from 'src/app/api/services';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';

const ServiceCategoryUpsertForm: React.FunctionComponent<AdminEditContainerProps<ServiceCategory>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    return (
        <KFormikForm initialValues={createUpsertServiceCategoryRequest(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={UpsertServiceCategoryRequestValidation}
        >
            <KFormikInput name="name"/>
            <KFormikInput name="color" as="color"/>
        </KFormikForm>
    )
}


export default ServiceCategoryUpsertForm;
