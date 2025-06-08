import React from 'react';
import {KFlexColumn} from 'src/app/shared/components/flex';

export interface KalendarioContainerProps {
    children: React.ReactNode;
}

export const KPageContainer: React.FunctionComponent<KalendarioContainerProps> = (
    {
        children,
    }) => {
    return (
        <div className="container mt-5">
            <KFlexColumn>
                {children}
            </KFlexColumn>
        </div>
    )
}
