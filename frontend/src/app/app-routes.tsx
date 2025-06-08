import EmployeeRoutes from 'src/app/modules/employee/employee-routes';
import {EMPLOYEE_ROUTES} from 'src/app/modules/employee/urls';
import React from 'react';
import {Route, Switch} from 'react-router-dom';
import AdminRoutes from 'src/app/modules/admin/admin-routes';
import {ADMIN_ROUTES} from 'src/app/modules/admin/urls';
import {AUTH_ROUTES} from 'src/app/modules/auth/urls';
import {USER_ROUTES} from 'src/app/modules/users/urls';
import UsersRoutes from 'src/app/modules/users/users-routes';
import AuthContainer from './modules/auth/auth-container';
import CompaniesRoutes from './modules/companies/companies-routes';
import HomeContainer from './modules/core/home/home-container';
import {ProtectedRoute} from './shared/util/router-extensions';


const AppRoutes: React.FunctionComponent = () => {
    return (
        <Switch>
            <Route path={AUTH_ROUTES.ROOT} component={AuthContainer}/>
            <Route path="/c" component={CompaniesRoutes}/>
            <ProtectedRoute path={USER_ROUTES.ROOT} component={UsersRoutes}/>
            <ProtectedRoute path={ADMIN_ROUTES.ROOT} component={AdminRoutes}/>
            <ProtectedRoute path={EMPLOYEE_ROUTES.ROOT} component={EmployeeRoutes}/>
            <Route path="/" component={HomeContainer}/>
        </Switch>
    )
}

export default AppRoutes;
