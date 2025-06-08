import React from 'react';
import {Route, Switch} from 'react-router-dom';
import CustomerDetailsContainer from 'src/app/modules/admin/customers/customer-details-container';
import CustomersContainer from 'src/app/modules/admin/customers/customers-container';
import {CUSTOMER_URLS} from 'src/app/modules/admin/customers/customers-urls';


const CustomersRoutes: React.FunctionComponent = () => {
    return (
        <Switch>
            <Route path={`${CUSTOMER_URLS.DETAILS}/:id`}
                   component={CustomerDetailsContainer}/>
            <Route path={CUSTOMER_URLS.LIST}
                   component={CustomersContainer}/>
        </Switch>
    )
}


export default CustomersRoutes;
