import React, {useState} from 'react';
import KIcon from 'src/app/shared/components/primitives/k-icon';
import _uniqueId from 'lodash/uniqueId';
import KTooltip from 'src/app/shared/components/primitives/k-tooltip';

interface KIconButtonProps {
    icon: string;
    onClick: () => void;
    color?: string;
    disabled?: boolean;
}

export const KIconButton: React.FunctionComponent<KIconButtonProps> = (
    {
        icon,
        onClick,
        color,
        disabled
    }) => {
    const [id] = useState(_uniqueId('icon-button-'));

    return (
        <div
            id={id}
        >
            <button onClick={onClick}
                    disabled={disabled}
                    type="button"
                    className={`c-${color} icon-button mx-1`}
            >
                <KIcon icon={icon}/>
            </button>
            {disabled &&
            <KTooltip id={id} text="restricted access"/>
            }
        </div>
    )
}
