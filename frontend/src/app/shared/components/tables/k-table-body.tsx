import React from 'react';
import {ColumnInstance, Row, TablePropGetter, TableProps} from 'react-table';

interface KTableBodyProps<D extends object> {
    getTableBodyProps: (propGetter?: TablePropGetter<D>) => TableProps;
    rows: Array<Row<D>>;
    prepareRow: (row: Row<D>) => void;
    visibleColumns: Array<ColumnInstance<D>>;
    renderRowSubComponent?: (row: Row<D>) => React.ReactNode;
}

function KTableBody<D extends object>(
    {
        getTableBodyProps,
        rows,
        prepareRow,
        visibleColumns,
        renderRowSubComponent
    }: KTableBodyProps<D>) {
    return (
        <tbody {...getTableBodyProps()}>
        {rows.map((row, i) => {
            prepareRow(row)
            return (
                <React.Fragment key={i}>
                    <tr {
                            // @ts-ignore
                            ...renderRowSubComponent ? row.getToggleRowExpandedProps() : row.getRowProps()
                        }>
                        {row.cells.map(cell =>
                            <td style={{verticalAlign: 'middle'}} {...cell.getCellProps()}>
                                {cell.render('Cell')}
                            </td>
                        )}
                    </tr>
                    {renderRowSubComponent &&
                    // @ts-ignore
                    row.isExpanded ? (
                        <tr {...row.getRowProps()}>
                            <td className="p-0" colSpan={visibleColumns.length}>
                                {renderRowSubComponent(row)}
                            </td>
                        </tr>
                    ) : null
                    }
                </React.Fragment>
            )
        })}
        </tbody>
    )
}


export default KTableBody;
