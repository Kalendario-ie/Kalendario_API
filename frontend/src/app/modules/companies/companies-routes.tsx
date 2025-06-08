import React, {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {Route, Switch, useParams, useRouteMatch} from 'react-router-dom';
import BookContainer from 'src/app/modules/companies/cart/book-container';
import CartContainer from 'src/app/modules/companies/cart/cart-container';
import CheckoutContainer from 'src/app/modules/companies/checkout/checkout-container';
import CompaniesContainer from 'src/app/modules/companies/companies-container';
import CreateCompanyContainer from 'src/app/modules/companies/create-company/create-company-container';
import {COMPANY_URLS} from 'src/app/modules/companies/paths';
import {ProtectedRoute} from 'src/app/shared/util/router-extensions';
import {companyDetailsRequest, selectCompany} from 'src/app/store/companies';

const CompaniesInnerRoutes: React.FunctionComponent = () => {
    let {path} = useRouteMatch();
    const {name} = useParams<{ name: string }>();
    const company = useSelector(selectCompany);
    const dispatch = useDispatch();

    useEffect(() => {
        if (company?.name !== name) {
            dispatch(companyDetailsRequest(name))
        }
    }, [dispatch, name, company])

    return (
        <Switch>
            <ProtectedRoute path={`${path}/book`} component={BookContainer}/>
            <ProtectedRoute path={`${path}/cart`} component={CartContainer}/>
            <ProtectedRoute path={`${path}/checkout`} component={CheckoutContainer}/>
            <Route path={`${path}/`} component={CompaniesContainer}/>
        </Switch>
    )
}

const CompaniesRoutes: React.FunctionComponent = () => {
    let {path} = useRouteMatch();
    return (
        <Switch>
            <Route path={COMPANY_URLS.CREATE} component={CreateCompanyContainer}/>
            <Route path={`${path}/:name`}>
                <CompaniesInnerRoutes/>
            </Route>
        </Switch>
    )
}

export default CompaniesRoutes;
