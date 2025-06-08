import React, {useEffect} from 'react';
import {useSelector} from 'react-redux';
import {Employee, upsertEmployeeRequestParser, UpsertEmployeeRequestValidation} from 'src/app/api/employees';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';
import {useAppDispatch} from 'src/app/store';
import {scheduleActions, scheduleSelectors} from 'src/app/store/admin/schedules';
import {serviceCategoryActions} from 'src/app/store/admin/serviceCategories';
import {serviceActions, serviceSelectors} from 'src/app/store/admin/services';

const EmployeeUpsertForm: React.FunctionComponent<AdminEditContainerProps<Employee>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const schedules = useSelector(scheduleSelectors.selectAll)
    const services = useSelector(serviceSelectors.selectServicesWithCategories)

    const dispatch = useAppDispatch();

    useEffect(() => {
        dispatch(scheduleActions.initializeStore());
        dispatch(serviceActions.initializeStore());
        dispatch(serviceCategoryActions.initializeStore());
    }, [dispatch]);

    return (
        <KFormikForm initialValues={upsertEmployeeRequestParser(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={UpsertEmployeeRequestValidation}
        >
            {entity?.photoUrl &&
            <KFlexRow className="mb-2" justify={'between'} align={'center'}>
                <KFlexRow className="flex-fill mr-2" justify={'center'} align={'center'}>
                    <AvatarImg size={5} src={entity.photoUrl}/>
                </KFlexRow>
                <KFlexColumn>
                    <KFormikInput name="firstName"/>
                    <KFormikInput name="lastName"/>
                </KFlexColumn>
            </KFlexRow>
            }
            <KFormikInput name="email"/>
            <KFormikInput name="phone"/>
            <KFormikInput name="instagram"/>
            <KFormikInput name="schedule" as={'select'} options={schedules}/>
            <KFormikInput name="services" as={'multi-select'} options={services}/>
        </KFormikForm>
    )
}


export default EmployeeUpsertForm;
