import React from 'react';

interface KFlexSpacerProps {
    size?: number;
}

export const KFlexSpacer: React.FunctionComponent<KFlexSpacerProps> = (
    {
        children,
        size= 2
    }) => {
    const style = {margin: `${size}rem`}
    return (
        <div style={style}>
        </div>
    )
}

