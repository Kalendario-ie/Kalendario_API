import React from 'react';
import {KFlexRow} from 'src/app/shared/components/flex';
import KFormikCancel from 'src/app/shared/components/forms/k-formik-cancel';
import {KFormikSubmit} from 'src/app/shared/components/forms/k-formik-submit';

interface KFormikStandardButtonsProps {
    onCancel: () => void;
}

const KFormikStandardButtons: React.FunctionComponent<KFormikStandardButtonsProps> = (
    {
        onCancel
    }) => {
    return (
        <KFlexRow align={'baseline'} justify={'end'}>
            <KFormikSubmit className="mr-2"/>
            <KFormikCancel className="m-0" onClick={onCancel}/>
        </KFlexRow>
    )
}


export default KFormikStandardButtons;
