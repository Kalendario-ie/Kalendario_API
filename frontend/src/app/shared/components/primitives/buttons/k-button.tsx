import React from 'react';
import {Button, CSSModule} from 'reactstrap';

interface KButtonProps
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

export const KButton: React.FunctionComponent<KButtonProps> = (props) => {
    return (
        <Button {...props}/>
    )
}
