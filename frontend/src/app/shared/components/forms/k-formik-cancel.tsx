import React, {HTMLProps} from 'react';
import {FormattedMessage} from 'react-intl';
import {KButton} from 'src/app/shared/components/primitives';

interface KFormikCancelProps extends HTMLProps<any> {
    onClick: () => void;
    className?: string;
}

const KFormikCancel: React.FunctionComponent<KFormikCancelProps> = (
    {
        onClick,
        className,
    }) => {
    return (
        <KButton className={className}
                 onClick={onClick}
                 color="danger"
                 type="button">
            <FormattedMessage id="COMMON.FORM.CANCEL"/>
        </KButton>
    )
}


export default KFormikCancel;
