import React from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {Slot} from 'src/app/api/companies';
import {companiesUrls} from 'src/app/modules/companies/paths';
import SlotsView from 'src/app/modules/companies/slots/slots-view';
import {momentToIso} from 'src/app/shared/util/moment-helpers';
import {useKHistory} from 'src/app/shared/util/router-extensions';
import {
    selectCompany,
    selectSelectedServiceId,
    selectSelectedSlotId,
    selectSlots,
    setSelectedSlotId
} from 'src/app/store/companies';

interface SlotsContainerProps {
}

const SlotsContainer: React.FunctionComponent<SlotsContainerProps> = () => {
    const company = useSelector(selectCompany);
    const serviceId = useSelector(selectSelectedServiceId);
    const slots = useSelector(selectSlots);
    const selectedSlotId = useSelector(selectSelectedSlotId);
    const dispatch = useDispatch();
    const useHistory = useKHistory();
    const isEmpty = !slots || Object.keys(slots).length === 0;


    const selectSlotOrAddToCart = (slot: Slot) => {
        if (!serviceId) {
            return;
        }
        if (slot.id !== selectedSlotId) {
            dispatch(setSelectedSlotId(slot.id))
            return;
        }
        if (company) {
            useHistory.push(companiesUrls(company).book({start: momentToIso(slot.start), service: +serviceId}))
        }
    }
    return (
        <>
            <SlotsView isEmpty={isEmpty}
                       slots={slots}
                       selectedSlotId={selectedSlotId}
                       onClick={selectSlotOrAddToCart}/>
        </>
    )
}


export default SlotsContainer;
