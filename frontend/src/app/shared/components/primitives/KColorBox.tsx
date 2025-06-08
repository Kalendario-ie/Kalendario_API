import React from 'react';

interface KColorBoxProps {
    backgroundColor: string;
}

const KColorBox: React.FunctionComponent<KColorBoxProps> = (
    {
        backgroundColor
    }) => {
    const style = {
        backgroundColor,
        minHeight: '2em',
        minWidth: '5em',
        borderRadius: '2px',
    }
    return (
        <div style={style}/>
    )
}


export default KColorBox;
