import React from 'react';
import {Switch} from 'react-router-dom';
import EmployeeDashboard from 'src/app/modules/employee/employee-dashboard';
import {EMPLOYEE_ROUTES} from 'src/app/modules/employee/urls';
import {ProtectedRoute} from 'src/app/shared/util/router-extensions';


const EmployeeRoutes: React.FunctionComponent = () => {
    return (
        <Switch>
            <ProtectedRoute path={EMPLOYEE_ROUTES.ROOT}
                            component={EmployeeDashboard}/>
        </Switch>
    )
}


export default EmployeeRoutes;
