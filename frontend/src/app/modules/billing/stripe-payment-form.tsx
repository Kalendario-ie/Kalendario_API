import {CardElement, useElements, useStripe} from '@stripe/react-stripe-js';
import React, {FormEvent, useState} from 'react';
import {FormattedMessage} from 'react-intl';
import {FormGroup} from 'reactstrap';
import {KButton, KCurrency, KErrorMessage} from 'src/app/shared/components/primitives';

interface StripePaymentFormProps {
    stripeSecret: string;
    price: number;
    onSuccess: () => void;
}

const StripePaymentForm: React.FunctionComponent<StripePaymentFormProps> = (
    {
        stripeSecret,
        price,
        onSuccess,
    }) => {
    const stripe = useStripe();
    const elements = useElements();
    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleSubmit = (event: FormEvent) => {
        // Block native form submission.
        event.preventDefault();
        if (!stripe || !elements) {
            // Stripe.js has not loaded yet. Make sure to disable
            // form submission until Stripe.js has loaded.
            return;
        }

        // Get a reference to a mounted CardElement. Elements knows how
        // to find your CardElement because there can only ever be one of
        // each type of element.
        const cardElement = elements.getElement(CardElement)!;

        setIsProcessing(true);
        setErrorMessage(undefined);

        // Use your card Element with other Stripe.js APIs
        stripe.confirmCardPayment(stripeSecret, {payment_method: {card: cardElement}})
            .then(({paymentIntent, error}) => {
                if (error) {
                    handleError(error.message);
                }
                if (paymentIntent) {
                    if (paymentIntent.status === 'succeeded') {
                        onSuccess();
                    } else {
                        handleError('something went wrong with your payment please try again later');
                    }
                }
            });
    };

    const handleError = (message: string | undefined) => {
        setErrorMessage(message);
        setIsProcessing(false);
    }

    return (
        <form onSubmit={handleSubmit}>
            <KErrorMessage message={errorMessage}/>
            <FormGroup>
                <CardElement className="form-control"
                             options={{
                                 style: {
                                     base: {
                                         fontSize: '1rem',
                                         color: '#424770',
                                         '::placeholder': {
                                             color: '#aab7c4',
                                         },
                                     },
                                     invalid: {
                                         color: '#9e2146',
                                     },
                                 },
                             }}
                />
            </FormGroup>
            <KButton block={true} color={'primary'} disabled={!stripe && isProcessing}>
                {isProcessing
                    ? <FormattedMessage id="COMMON.FORM.PROCESSING"/>
                    : <><FormattedMessage id="PAYMENTS.PAY"/> <KCurrency value={price}/></>
                }
            </KButton>
        </form>
    )
}


export default StripePaymentForm;
