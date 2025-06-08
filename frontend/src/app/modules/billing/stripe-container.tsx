import React from 'react';
import {FormattedMessage} from 'react-intl';
import StripePaymentForm from 'src/app/modules/billing/stripe-payment-form';
import KModal from 'src/app/shared/components/modal/k-modal';

interface StripeContainerProps {
    price: number;
    stripeSecret: string;
    isOpen: boolean;
    onSuccess: () => void;
    cancelClick: () => void;
}

const StripeContainer: React.FunctionComponent<StripeContainerProps> = (
    {
        isOpen,
        price,
        stripeSecret,
        onSuccess,
        cancelClick
    }) => {

    return (
        <KModal
            header={<FormattedMessage id="PAYMENTS.HEADER"/>}
            body={<StripePaymentForm stripeSecret={stripeSecret}
                                     price={price}
                                     onSuccess={onSuccess}/>}
            onCancel={cancelClick}
            isOpen={isOpen}
        />
    )
}


export default StripeContainer;
