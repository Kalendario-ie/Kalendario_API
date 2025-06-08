import React, {useMemo} from 'react';
import {adminEmployeeClient, Employee} from 'src/app/api/employees';
import EmployeeRowExpanded from 'src/app/modules/admin/employees/employee-row-expanded';
import {AdminTableContainerProps} from 'src/app/shared/admin/interfaces';
import EditableAvatarImg from 'src/app/shared/components/primitives/containers/editable-avatar-img';
import KTable from 'src/app/shared/components/tables/k-table';
import {ExpanderColumn} from 'src/app/shared/components/tables/k-table-row-expander';
import KTextColumnFilter from 'src/app/shared/components/tables/k-text-column-filter';
import {useAppDispatch} from 'src/app/store';
import {employeeReducerActions} from 'src/app/store/admin/employees';


const EmployeesTable: React.FunctionComponent<AdminTableContainerProps<Employee>> = (
    {
        entities,
        buttonsColumn,
        filter,
    }) => {
    const dispatch = useAppDispatch();


    const columns = useMemo(() => {
        const handleFileSubmit = (entity: Employee, file: File) =>
            adminEmployeeClient.uploadProfilePicture(entity.id, file)
                .then(res => {
                    dispatch(employeeReducerActions.upsertOne({...entity, photoUrl: res.url}));
                    return true;
                })
                .catch(error => false);

        return [
            ExpanderColumn,
            {
                Header: 'Photo',
                accessor: 'photoUrl',
                Cell: (value: any) => <EditableAvatarImg src={value.cell.value}
                                                         onSubmit={(file) => handleFileSubmit(value.row.original, file)}
                                                         size={3}/>
            },
            {
                Header: 'Name',
                accessor: 'name',
                Filter: KTextColumnFilter
            },
            {
                Header: 'Email',
                accessor: 'email',
                Filter: KTextColumnFilter
            },
            {
                Header: 'Phone',
                accessor: 'phone',
                Filter: KTextColumnFilter
            },
            {
                Header: 'Instagram',
                accessor: 'instagram',
            },
            buttonsColumn
        ]
    }, [buttonsColumn, dispatch])


    const renderRowSubComponent = React.useCallback(
        (row: any) => <EmployeeRowExpanded employee={row.original}/>, [])

    return (
        <KTable columns={columns}
                data={entities}
                renderRowSubComponent={renderRowSubComponent}
                hover={true}
        />
    )
}


export default EmployeesTable;
