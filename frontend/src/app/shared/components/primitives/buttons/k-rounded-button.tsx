import React from 'react';
import {CSSModule} from 'reactstrap';
import {KButton} from 'src/app/shared/components/primitives/buttons/k-button';

interface KRoundedButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    [key: string]: any;
    outline?: boolean;
    active?: boolean;
    block?: boolean;
    color?: string;
    tag?: React.ElementType;
    innerRef?: React.Ref<HTMLButtonElement>;
    size?: string;
    cssModule?: CSSModule;
    close?: boolean;
}

export const KRoundedButton: React.FunctionComponent<KRoundedButtonProps> = ({children, className = '', ...rest}) => {
    return (
        <KButton className={`${className} btn-round`} {...rest}>
            {children}
        </KButton>
    )
}
