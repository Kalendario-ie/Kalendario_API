import React from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {Redirect, useHistory} from 'react-router-dom';
import CartCompanySummary from 'src/app/modules/companies/cart/cart-company-summary';
import CartRequestSummary from 'src/app/modules/companies/cart/cart-request-summary';
import {companiesUrls} from 'src/app/modules/companies/paths';
import KGrid from 'src/app/shared/components/grid/k-grid';
import {KPageContainer, KCard} from 'src/app/shared/components/primitives/containers';
import {
    addNotesRequest,
    deleteAppointmentRequest,
    selectCartIsLoadedAndEmpty,
    selectCompany,
    selectCurrentRequest
} from 'src/app/store/companies';

interface CartContainerProps {
}

const CartContainer: React.FunctionComponent<CartContainerProps> = () => {
    const request = useSelector(selectCurrentRequest)
    const company = useSelector(selectCompany);
    const cartIsLoadedAndEmpty = useSelector(selectCartIsLoadedAndEmpty);
    const dispatch = useDispatch();
    const history = useHistory();

    const proceedToCheckout = (notes: string) => {
        if (!company || !request) return;
        dispatch(addNotesRequest({id: request.id, notes}));
        history.push(companiesUrls(company).checkout)
    }

    return (
        <KPageContainer>
            {company && request &&
            <>
                {cartIsLoadedAndEmpty &&
                <Redirect to={companiesUrls(company).index}/>
                }
                <KGrid size={6} smSize={12}>
                    <KCard>
                        <CartRequestSummary request={request}
                                            deleteClick={(id => dispatch(deleteAppointmentRequest(id)))}
                        />
                    </KCard>
                    <CartCompanySummary company={company}
                                        request={request}
                                        proceedToCheckoutClick={proceedToCheckout}
                    />
                </KGrid>
            </>
            }
        </KPageContainer>
    )
}


export default CartContainer;
