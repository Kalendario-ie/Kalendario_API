import React, {HTMLProps} from 'react';
import {FlexAlign, FlexJustify} from 'src/app/shared/components/flex/types';

interface KFlexRowProps extends HTMLProps<any> {
    justify?: FlexJustify;
    align?: FlexAlign;
    flexWrap?: boolean;
}

export const KFlexRow: React.FunctionComponent<KFlexRowProps> = (
    {
        children,
        justify,
        align,
        className= '',
        flexWrap = false,
        ...rest
    }) => {
    className += ` d-flex flex-row${flexWrap ? ' flex-wrap' : ''}`;
    if (justify) {
        className += ` justify-content-${justify}`;
    }
    if (align)  {
        className += ` align-items-${align}`;
    }
    return (
        <div className={className} {...rest}>{children}</div>
    )
}
