import React from 'react';
import {KFlexRow} from 'src/app/shared/components/flex';

interface KIconProps {
    icon: string;
    color?: string;
    margin?: number;
    text?: string;
}

const KIcon: React.FunctionComponent<KIconProps> = (
    {
        icon,
        color,
        margin = 1,
        text
    }) => {
    const className = `fa fa-${icon} c-${color} mx-${margin}`;
    const iconElement = <i className={className}/>;
    return (
        <>
            {!text &&
            iconElement
            }
            {text &&
            <KFlexRow align={'center'}>
                {iconElement} {text}
            </KFlexRow>
            }
        </>
    )
}


export default KIcon;
