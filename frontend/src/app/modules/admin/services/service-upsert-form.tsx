import React from 'react';
import {PermissionModel, PermissionType} from 'src/app/api/auth';
import {createUpsertServiceRequest, Service} from 'src/app/api/services';
import {UpsertServiceRequestValidation} from 'src/app/api/services/requests';
import AdminButton from 'src/app/shared/admin/admin-button';
import {useEditModal} from 'src/app/shared/admin/hooks';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFlexRow} from 'src/app/shared/components/flex';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import {useAppSelector} from 'src/app/store';
import {serviceCategoryActions, serviceCategorySelectors} from 'src/app/store/admin/serviceCategories';
import ServiceCategoryUpsertForm from './service-category-upsert-form';

const ServiceUpsertForm: React.FunctionComponent<AdminEditContainerProps<Service>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const serviceCategories = useAppSelector(serviceCategorySelectors.selectAll)
    const [openModal, modal] = useEditModal(serviceCategorySelectors, serviceCategoryActions, ServiceCategoryUpsertForm);

    const serviceCategory = (id: number) => serviceCategories.find(sc => sc.id === id) || null

    return (
        <KFormikForm initialValues={createUpsertServiceRequest(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={UpsertServiceRequestValidation}
        >
            {(formik) =>
                <>
                    {modal}
                    <KFlexRow align={'center'} justify={'center'}>
                        <KFormikInput className="flex-fill" name="category" as={'select'} options={serviceCategories}/>
                        <AdminButton type={PermissionType.change}
                                     model={PermissionModel.servicecategory}
                                     onClick={openModal(serviceCategory(formik.getFieldProps('category').value))}/>
                        <AdminButton type={PermissionType.add}
                                     model={PermissionModel.servicecategory}
                                     onClick={openModal(null)}/>
                    </KFlexRow>
                    <KFormikInput name="name"/>
                    <KFormikInput name="duration" as="duration"/>
                    <KFormikInput name="color" as="color"/>
                    <KFormikInput name="description"/>
                    <KFormikInput name="cost" type="number"/>
                </>
            }

        </KFormikForm>
    )
}


export default ServiceUpsertForm;
