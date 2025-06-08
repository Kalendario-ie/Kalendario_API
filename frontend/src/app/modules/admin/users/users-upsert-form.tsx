import React from 'react';
import {upsertUserRequestParser, UpsertUserRequestValidation, AdminUser} from 'src/app/api/users';
import ChangePasswordForm from 'src/app/modules/admin/users/change-password-form';
import {useSelectAll} from 'src/app/shared/admin/hooks';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import {employeeActions, employeeSelectors} from 'src/app/store/admin/employees';
import {permissionGroupActions, permissionGroupSelectors} from 'src/app/store/admin/permissionGroups';


const UsersUpsertForm: React.FunctionComponent<AdminEditContainerProps<AdminUser>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const employees = useSelectAll(employeeSelectors, employeeActions);
    const groups = useSelectAll(permissionGroupSelectors, permissionGroupActions);

    return (
        <KFormikForm initialValues={upsertUserRequestParser(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={UpsertUserRequestValidation}
        >
            {entity?.id &&
            <ChangePasswordForm id={entity.id}/>
            }
            <KFormikInput name="firstName"/>
            <KFormikInput name="lastName"/>
            <KFormikInput name="email"/>
            <KFormikInput name="groups" as={'multi-select'} options={groups}/>
            <KFormikInput name="employee" as={'select'} options={employees}/>
        </KFormikForm>
    )
}


export default UsersUpsertForm;
