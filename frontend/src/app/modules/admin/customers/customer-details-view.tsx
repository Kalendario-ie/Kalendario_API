import React from 'react';
import {Customer} from 'src/app/api/customers';
import {KFlexColumn} from 'src/app/shared/components/flex';
import KIcon from 'src/app/shared/components/primitives/k-icon';

interface CustomerDetailsViewProps {
    customer: Customer;
}

const CustomerDetailsView: React.FunctionComponent<CustomerDetailsViewProps> = (
    {
        customer
    }) => {
    return (
        <KFlexColumn>
            <KIcon icon="user" text={customer.name}/>
            <KIcon icon="phone" text={customer.phone}/>
            <KIcon icon="at" text={customer.email}/>
            <KIcon icon="exclamation" text={customer.warning}/>
        </KFlexColumn>
    )
}


export default CustomerDetailsView;
