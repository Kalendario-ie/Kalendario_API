import React from 'react';
import {Column, Row, useExpanded, useFilters, useTable} from 'react-table';
import {Table} from 'reactstrap';
import {KDefaultColumnFilter} from 'src/app/shared/components/tables/k-default-column-filter';
import KTableBody from 'src/app/shared/components/tables/k-table-body';
import KTableHeader from 'src/app/shared/components/tables/k-table-header';
import style from './k-table.module.scss';

interface KTableProps<D extends object> {
    columns: Array<Column<D>>
    data: D[]
    renderRowSubComponent?: (row: Row<D>) => React.ReactNode
    hover?: boolean;
    stripped?: boolean;
    extraPrepare?: (row: Row<D>) => void;
}

function KTable<D extends object>(
    {
        columns,
        data,
        renderRowSubComponent,
        hover = false,
        stripped = false,
        extraPrepare,
    }: KTableProps<D>) {
    const filterTypes = React.useMemo(
        () => ({
            text: (rows: any[], id: number, filterValue: string) => {
                return rows.filter(row => {
                    const rowValue = row.values[id]
                    return rowValue !== undefined
                        ? String(rowValue)
                            .toLowerCase()
                            .startsWith(filterValue.toLowerCase())
                        : true
                })
            },
        }),
        []
    )
    const defaultColumn = React.useMemo(() => ({Filter: KDefaultColumnFilter,}), [])

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        visibleColumns,
    } = useTable(
        {
            columns,
            data,
            // @ts-ignore
            defaultColumn,
            filterTypes,
            autoResetFilters: false
        },
        useFilters,
        useExpanded,
    )

    const customPrepareRow = (row: Row<D>) => {
        prepareRow(row);
        extraPrepare && extraPrepare(row);
    }


    return (
        <Table className={style.fixedHeaders} hover={hover} striped={stripped} {...getTableProps()}>
            <KTableHeader headerGroups={headerGroups}
            />
            <KTableBody getTableBodyProps={getTableBodyProps}
                        rows={rows}
                        prepareRow={customPrepareRow}
                        visibleColumns={visibleColumns}
                        renderRowSubComponent={renderRowSubComponent}
            />
        </Table>
    )
}


export default KTable;
