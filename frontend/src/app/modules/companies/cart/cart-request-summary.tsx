import React from 'react';
import {FormattedMessage} from 'react-intl';
import {RequestModel} from 'src/app/api/requests';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';
import { KFlexColumn, KFlexRow } from 'src/app/shared/components/flex';
import {stringToMoment} from 'src/app/shared/util/moment-helpers';

interface CartRequestSummaryProps {
    request: RequestModel;
    showDelete?: boolean;
    deleteClick?: (id: number) => void;
}

const CartRequestSummary: React.FunctionComponent<CartRequestSummaryProps> = (
    {
        request,
        showDelete = true,
        deleteClick = () => {
        }
    }) => {
    const isEmpty = !request || (request && request.itemsCount === 0);
    return (
        <KFlexColumn>
            {request.items.map((requestItem, key) => (
                    <KFlexRow align="center" key={key}>
                        <AvatarImg className="mr-4" src={requestItem.employee.photoUrl}/>
                        <KFlexColumn className="w-100">
                            <h4 className="border-bottom border-dark">{requestItem.employee.name}</h4>
                            {requestItem.appointments.map((appointment, key) => (
                                    <KFlexRow className="m-2" key={key} justify={'between'}>
                                        <KFlexColumn>
                                            <h6>{appointment.service.name}</h6>
                                            {stringToMoment(appointment.start).format('DD/MM/YYYY - HH:mm')}
                                            (duration: {appointment.service.duration.minute})
                                        </KFlexColumn>
                                        <KFlexColumn className="text-right">
                                            <h6 className="c-primary">{appointment.service.price}</h6>
                                            {showDelete &&
                                            <button className="btn btn-sm btn-outline-danger"
                                                    onClick={() => deleteClick(appointment.id)}
                                            >
                                                <i className="fa fa-trash"/>
                                            </button>
                                            }
                                        </KFlexColumn>
                                    </KFlexRow>
                                )
                            )}
                        </KFlexColumn>
                    </KFlexRow>
                )
            )}
            <div className="text-right font-weight-bold m-2 c-primary">
                Total: {request.total.toFixed(2)}
            </div>
            {isEmpty && <FormattedMessage id="COMPANY.EMPTY-CART"/>}
        </KFlexColumn>
    )
}

export default CartRequestSummary;

