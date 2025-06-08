import React from 'react';

interface KGridProps {
    size?: number;
    smSize?: number;
    mdSize?: number;
    lgSize?: number;
    xlSize?: number;
    children: React.ReactNode[];
}

const KGrid: React.FunctionComponent<KGridProps> = (
    {
        size = 12,
        smSize,
        mdSize,
        lgSize,
        xlSize,
        children
    }) => {
    const className = `col-sm-${smSize || size} col-md-${mdSize || size} col-lg-${lgSize || size} col-xl-${xlSize || size}`;
    return (
        <div className="row">
            {children && children.map((node, k) =>
                <div key={k} className={className}>{node}</div>)}
        </div>
    )
}


export default KGrid;
