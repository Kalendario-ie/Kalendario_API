import React from 'react';
import {Employee} from 'src/app/api/employees';
import ServicesCard from 'src/app/modules/admin/employees/services-card';
import {KFlexRow} from 'src/app/shared/components/flex';

interface EmployeeRowExpandedProps {
    employee: Employee;
}

const EmployeeRowExpanded: React.FunctionComponent<EmployeeRowExpandedProps> = (
    {
        employee
    }) => {
    return (
        <KFlexRow>
            <ServicesCard serviceIds={employee.services}/>
        </KFlexRow>
    )
}


export default EmployeeRowExpanded;
