import React, {useState} from 'react';
import {FormattedMessage} from 'react-intl';
import {useDispatch, useSelector} from 'react-redux';
import {Redirect} from 'react-router-dom';
import {billingClient} from 'src/app/api/billing';
import {RequestModel} from 'src/app/api/requests';
import StripeContainer from 'src/app/modules/billing/stripe-container';
import CompanyAvatar from 'src/app/modules/companies/avatar/company-avatar';
import CartRequestSummary from 'src/app/modules/companies/cart/cart-request-summary';
import {companiesUrls} from 'src/app/modules/companies/paths';
import {USER_ROUTES} from 'src/app/modules/users/urls';
import {KFlexSpacer} from 'src/app/shared/components/flex';
import {KCard, KPageContainer} from 'src/app/shared/components/primitives/containers';
import {useKHistory} from 'src/app/shared/util/router-extensions';
import {
    confirmCartRequest,
    selectCartIsLoadedAndEmpty,
    selectCompany,
    selectCurrentRequest
} from 'src/app/store/companies';


const CheckoutContainer: React.FunctionComponent = () => {
    const company = useSelector(selectCompany);
    const request = useSelector(selectCurrentRequest);
    const cartIsLoadedAndEmpty = useSelector(selectCartIsLoadedAndEmpty);
    const [stripePaymentOpen, setStripePaymentOpen] = useState(false);
    const [stripeSecret, setStripeSecret] = useState<string>('');
    const dispatch = useDispatch();
    const history = useKHistory();

    const confirmRequest = (request: RequestModel) => () => {
        dispatch(confirmCartRequest(request.id));
        history.push(USER_ROUTES.BOOKING(request.scheduledDate));
    }

    const toggleStripePaymentOpen = (id: number) => () => {
        billingClient.payment(id)
            .then(res => {
                setStripeSecret(res.clientSecret);
                setStripePaymentOpen(!stripePaymentOpen)
            })
        ;
    }

    return (
        <KPageContainer>
            {company && request &&
            <>
                {cartIsLoadedAndEmpty &&
                <Redirect to={companiesUrls(company).index}/>
                }
                <KCard>
                    <>
                        <CompanyAvatar company={company}/>
                        <KFlexSpacer/>
                        <CartRequestSummary request={request} showDelete={false}/>
                        <KFlexSpacer/>
                        <h4><FormattedMessage id="COMPANY.NOTES"/></h4>
                        {request.customerNotes}
                        <KFlexSpacer/>
                        <>
                            {company.config.canReceiveCardPayments &&
                            <button onClick={toggleStripePaymentOpen(request.id)}
                                    className="btn btn-primary mr-2">
                                <FormattedMessage id="COMPANY.PAY-CARD"/>
                            </button>
                            }
                            {company.config.canReceiveUnpaidRequest &&
                            <button className="btn btn-accent"
                                    onClick={confirmRequest(request)}>
                                <FormattedMessage id="COMPANY.PAY-CASH"/>
                            </button>
                            }
                        </>
                    </>
                </KCard>
                <StripeContainer
                    price={request.total}
                    stripeSecret={stripeSecret}
                    isOpen={stripePaymentOpen}
                    onSuccess={confirmRequest(request)}
                    cancelClick={() => setStripePaymentOpen(false)}
                />
            </>

            }
        </KPageContainer>
    )
}


export default CheckoutContainer;
