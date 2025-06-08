import React from 'react';

interface KFlexRowItemProps {
    children: React.ReactNode;
    grow?: number;
    basisPercent?: number;
}

interface FlexStyle {
    flexGrow?: number;
    flex?: string;
}

export const KFlexRowItem: React.FunctionComponent<KFlexRowItemProps> = (
    {
        children,
        grow,
        basisPercent
    }) => {
    const style: FlexStyle = {};
    if (grow) {
        style.flexGrow = grow;
    }
    if (basisPercent) {
        style.flex = `${basisPercent}%`
    }
    return (
        <div style={style}>
            {children}
        </div>
    )
}
