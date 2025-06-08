import {AdminUser} from 'src/app/api/users';
import React, {useMemo} from 'react';
import {AdminTableContainerProps} from 'src/app/shared/admin/interfaces';
import KTable from 'src/app/shared/components/tables/k-table';
import KTextColumnFilter from 'src/app/shared/components/tables/k-text-column-filter';

const UsersTable: React.FunctionComponent<AdminTableContainerProps<AdminUser>> = (
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
            {
                Header: 'Email',
                accessor: 'email',
            },
            {
                Header: 'Phone',
                accessor: 'phone',
            },
            buttonsColumn
        ], [buttonsColumn, filter])

    return (
        <KTable columns={columns} data={entities}/>
    )
}


export default UsersTable;
