import React from 'react';
import {Route, Switch} from 'react-router-dom';
import BookingsContainer from 'src/app/modules/users/bookings/bookings-container';
import {USER_ROUTES} from 'src/app/modules/users/urls';

const UsersRoutes: React.FunctionComponent = () => {
    return (
        <Switch>
            <Route path={USER_ROUTES.BOOKING()} component={BookingsContainer}/>
        </Switch>
    )
}


export default UsersRoutes;
