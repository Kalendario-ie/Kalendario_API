import React from 'react';

interface KTextButtonProps
    extends React.ButtonHTMLAttributes<HTMLDivElement> {
}

export const KTextButton: React.FunctionComponent<KTextButtonProps> = (
    {
        children,
        className,
        onClick,
        ...rest
    }) => {
    return (
        <div className={`m-2 c-pointer ${className}`}
             onClick={onClick}
             {...rest}
        >
            {children}
        </div>
    )
}
