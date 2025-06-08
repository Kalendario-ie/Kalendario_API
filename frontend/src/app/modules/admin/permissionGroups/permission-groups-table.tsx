import {PermissionGroup} from 'src/app/api/permissions';
import React, {useMemo} from 'react';
import {AdminTableContainerProps} from 'src/app/shared/admin/interfaces';
import KTable from 'src/app/shared/components/tables/k-table';
import KTextColumnFilter from 'src/app/shared/components/tables/k-text-column-filter';

const PermissionGroupsTable: React.FunctionComponent<AdminTableContainerProps<PermissionGroup>> = (
    {
        entities,
        buttonsColumn,
        filter,
    }) => {
    const columns =
        useMemo(() => [
            {
                Header: 'Name',
                accessor: 'name',
                Filter: (cell: any) => <KTextColumnFilter {...cell} onChangeSideEffect={filter}/>
            },
            buttonsColumn
        ], [buttonsColumn, filter])

    return (
        <KTable columns={columns} data={entities}/>
    )
}


export default PermissionGroupsTable;
