import React from 'react';
import {SchedulingPanel} from 'src/app/api/scheduling-panels/models';
import {upsertSchedulingPanelRequestParser} from 'src/app/api/scheduling-panels/parsers';
import {useSelectAll} from 'src/app/shared/admin/hooks';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import {employeeActions, employeeSelectors} from 'src/app/store/admin/employees';

const SchedulingPanelForm: React.FunctionComponent<AdminEditContainerProps<SchedulingPanel>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const employees = useSelectAll(employeeSelectors, employeeActions);

    return (
        <KFormikForm initialValues={upsertSchedulingPanelRequestParser(entity)}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
        >
            <KFormikInput name="name"/>
            <KFormikInput name="employees" as="multi-select" options={employees}/>
        </KFormikForm>
    )
}


export default SchedulingPanelForm;
