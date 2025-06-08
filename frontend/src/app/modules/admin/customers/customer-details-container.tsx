import React, {useEffect} from 'react';
import {FormattedMessage} from 'react-intl';
import {useParams} from 'react-router-dom';
import CustomerAppointments from 'src/app/modules/admin/customers/customer-appointments';
import CustomerDetailsView from 'src/app/modules/admin/customers/customer-details-view';
import {CUSTOMER_URLS} from 'src/app/modules/admin/customers/customers-urls';
import {KFlexRow} from 'src/app/shared/components/flex';
import {KButton} from 'src/app/shared/components/primitives';
import {KCard} from 'src/app/shared/components/primitives/containers';
import {useKHistory} from 'src/app/shared/util/router-extensions';
import {useAppDispatch, useAppSelector} from 'src/app/store';
import {customerActions, customerSelectors} from 'src/app/store/admin/customers';

interface CustomerDetailsContainerProps {
}

const CustomerDetailsContainer: React.FunctionComponent<CustomerDetailsContainerProps> = () => {
    const {id} = useParams<{ id: string }>();
    const customer = useAppSelector(state => customerSelectors.selectById(state, +id));
    const dispatch = useAppDispatch();
    const history = useKHistory();

    useEffect(() => {
        if (!customer && !!id) {
            dispatch(customerActions.fetchEntity(+id));
        }
    }, [dispatch, id, customer]);

    const handleBackClick = () => history.push(CUSTOMER_URLS.LIST);

    return (
        <>
            {customer &&
            <>
                <KCard hasShadow={false}
                       className="m-2"
                       header={
                           <KFlexRow justify="between">
                               <FormattedMessage id="ADMIN.COMMON.CUSTOMER-DETAILS"/>
                               <KButton color="primary" onClick={handleBackClick}>
                                   <FormattedMessage id="ADMIN.COMMON.BACK-TO-LIST"/>
                               </KButton>
                           </KFlexRow>
                       }>

                    <CustomerDetailsView customer={customer}/>
                    <CustomerAppointments customer={customer}/>
                </KCard>
            </>
            }
        </>
    )
}


export default CustomerDetailsContainer;
