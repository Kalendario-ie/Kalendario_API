import React from 'react';
import {useIntl} from 'react-intl';
import {Switch} from 'react-router-dom';
import {PermissionModel} from 'src/app/api/auth';
import AppointmentsContainer from 'src/app/modules/admin/appointments/appointments-container';
import CustomersRoutes from 'src/app/modules/admin/customers/customers-routes';
import EmployeesContainer from 'src/app/modules/admin/employees/employees-container';
import PermissionGroupsContainer from 'src/app/modules/admin/permissionGroups/permission-groups-container';
import SchedulesContainer from 'src/app/modules/admin/schedules/schedules-container';
import ServicesContainer from 'src/app/modules/admin/services/services-container';
import {ADMIN_ROUTES} from 'src/app/modules/admin/urls';
import UsersContainer from 'src/app/modules/admin/users/users-container';
import KDashboardContainer from 'src/app/shared/components/dashboard/k-dashboard-container';
import {SideBarLinks} from 'src/app/shared/components/dashboard/k-dashboard-sidebar';
import {ProtectedRoute} from 'src/app/shared/util/router-extensions';


const AdminRoutes: React.FunctionComponent = () => {
    const intl = useIntl();
    const links: SideBarLinks = ({
        'Main': [
            // [intl.formatMessage({id: 'ADMIN.COMMON.HOME'}), ADMIN_ROUTES.HOME, 'home'],
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.SERVICES'}),
                url: ADMIN_ROUTES.SERVICES,
                icon: 'magic',
                permissionModel: PermissionModel.service
            },
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.SCHEDULES'}),
                url: ADMIN_ROUTES.SCHEDULES,
                icon: 'calendar-alt',
                permissionModel: PermissionModel.schedule
            },
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.EMPLOYEES'}),
                url: ADMIN_ROUTES.EMPLOYEES,
                icon: 'people-carry',
                permissionModel: PermissionModel.employee
            },
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.CUSTOMERS'}),
                url: ADMIN_ROUTES.CUSTOMERS,
                icon: 'address-card',
                permissionModel: PermissionModel.customer
            },
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.APPOINTMENTS'}),
                url: ADMIN_ROUTES.APPOINTMENTS,
                icon: 'address-book',
                permissionModel: PermissionModel.appointment
            },
        ],
        'Manage': [

            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.USERS'}),
                url: ADMIN_ROUTES.USERS,
                icon: 'users',
                permissionModel: PermissionModel.user
            },
            {
                name: intl.formatMessage({id: 'ADMIN.COMMON.PERMISSION-GROUPS'}),
                url: ADMIN_ROUTES.PERMISSION_GROUPS,
                icon: 'users-slash',
                permissionModel: PermissionModel.groupprofile
            },
        ]
    });

    return (
        <>
            {links &&
            <KDashboardContainer links={links}>
                <Switch>
                    <ProtectedRoute permissionModel={PermissionModel.service}
                                    path={ADMIN_ROUTES.SERVICES}
                                    component={ServicesContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.employee}
                                    path={ADMIN_ROUTES.EMPLOYEES}
                                    component={EmployeesContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.customer}
                                    path={ADMIN_ROUTES.CUSTOMERS}
                                    component={CustomersRoutes}/>

                    <ProtectedRoute permissionModel={PermissionModel.schedule}
                                    path={ADMIN_ROUTES.SCHEDULES}
                                    component={SchedulesContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.user}
                                    path={ADMIN_ROUTES.USERS}
                                    component={UsersContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.groupprofile}
                                    path={ADMIN_ROUTES.PERMISSION_GROUPS}
                                    component={PermissionGroupsContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.appointment}
                                    path={ADMIN_ROUTES.APPOINTMENTS}
                                    component={AppointmentsContainer}/>

                    <ProtectedRoute permissionModel={PermissionModel.service}
                                    path={ADMIN_ROUTES.ROOT}
                                    component={ServicesContainer}/>
                </Switch>
            </KDashboardContainer>
            }
        </>
    )
}


export default AdminRoutes;
