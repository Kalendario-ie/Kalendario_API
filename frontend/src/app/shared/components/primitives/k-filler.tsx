import React from 'react';

interface KFillerProps {
    className?: string;
}

const KFiller: React.FunctionComponent<KFillerProps> = (props) => {
    const style: React.CSSProperties = {
        boxSizing: 'content-box'
    }
    return (
        <div style={style} {...props}/>
    )
}


export default KFiller;
