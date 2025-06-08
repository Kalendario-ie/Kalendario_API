import React, {useState} from 'react';
import {KFlexRow} from 'src/app/shared/components/flex';

interface KShowOnHoverContainerProps {
    children: React.ReactNode;
    className?: string;
    style?: React.CSSProperties;
}

const KShowOnHoverContainer: React.FunctionComponent<KShowOnHoverContainerProps> = (
    {
        children,
        className,
        style
    }) => {
    const [showContent, setShowContent] = useState(false);

    const handleMouseEnter = () => setShowContent(true);
    const handleMouseOut = () => setShowContent(false);
    return (
        <KFlexRow
            align={'center'}
            justify={'center'}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseOut}
            className={`${className} position-relative`}
            style={style}
        >
            {showContent &&
            children
            }
        </KFlexRow>
    )
}


export default KShowOnHoverContainer;
