import React from 'react';
import {Service} from 'src/app/api/services';
import DateSelectorContainer from 'src/app/modules/companies/date-selector/date-selector-container';
import SlotsContainer from 'src/app/modules/companies/slots/slots-container';
import KModal from 'src/app/shared/components/modal/k-modal';

interface SlotsForServiceModalProps {
    service: Service | null | undefined;
    onCancel: () => void;
}

const SlotsForServiceModal: React.FunctionComponent<SlotsForServiceModalProps> = (
    {
        service,
        onCancel
    }) => {
    return (
        <KModal isOpen={!!service}
                header={<DateSelectorContainer/>}
                body={<SlotsContainer/>}
                onCancel={onCancel}
        />
    )
}


export default SlotsForServiceModal;
