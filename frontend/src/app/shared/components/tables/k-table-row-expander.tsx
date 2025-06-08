import React from 'react';
import KIcon from 'src/app/shared/components/primitives/k-icon';

const KTableRowExpander: React.FunctionComponent = (props: any) => {
    return (
        <span>
            {props.row.isExpanded ? <KIcon icon="caret-down"/> : <KIcon icon="caret-right"/>}
        </span>
    )
}


export const ExpanderColumn = {
    Header: () => null, // No header
    id: 'expander', // It needs an ID
    Cell: (value: any) => <KTableRowExpander {...value}/>,
};
