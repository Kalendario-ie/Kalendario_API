import React, {useState} from 'react';
import {FormattedMessage, useIntl} from 'react-intl';
import {CompanyDetails} from 'src/app/api/companies';
import {RequestModel} from 'src/app/api/requests';
import CompanyAvatar from 'src/app/modules/companies/avatar/company-avatar';
import {KInput} from 'src/app/shared/components/primitives/inputs';
import {KCard} from 'src/app/shared/components/primitives/containers';

interface CartSummaryProps {
    company: CompanyDetails;
    request: RequestModel,
    proceedToCheckoutClick: (notes: string) => void;
}

const CartCompanySummary: React.FunctionComponent<CartSummaryProps> = (
    {
        company,
        request,
        proceedToCheckoutClick
    }) => {
    const intl = useIntl();
    const [notes, setNotes] = useState(request.customerNotes || '');

    return (
        <KCard>
            <CompanyAvatar company={company}/>
            <p>
                {company.config.preBookWarn}
            </p>
            <KInput className="mb-2"
                    type="textarea"
                    value={notes}
                    onChange={event => setNotes(event.target.value)}
                    placeholder={intl.formatMessage({id: 'COMPANY.ADD-NOTES'})}/>

            <button className="btn btn-primary btn-block" onClick={() => proceedToCheckoutClick(notes)}>
                <FormattedMessage id="COMPANY.PROCEED-CHECKOUT"/>
            </button>
        </KCard>
    )
}


export default CartCompanySummary;
