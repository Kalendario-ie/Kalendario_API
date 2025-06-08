import React from 'react';
import {PermissionModel} from 'src/app/api/auth';
import CustomerUpsertForm from 'src/app/modules/admin/customers/customer-upsert-form';
import CustomersTable from 'src/app/modules/admin/customers/customers-table';
import {CUSTOMER_URLS} from 'src/app/modules/admin/customers/customers-urls';
import AdminListEditContainer from 'src/app/shared/admin/admin-list-edit-container';
import {useAppDispatch} from 'src/app/store';
import {customerActions, customerSelectors} from 'src/app/store/admin/customers';


const CustomersContainer: React.FunctionComponent = () => {
    const dispatch = useAppDispatch()

    const filter = React.useMemo(() =>
        (value: string | undefined) => {
            dispatch(customerActions.fetchEntities({search: value}));
        }, [dispatch]);

    return (
        <AdminListEditContainer baseSelectors={customerSelectors}
                                baseActions={customerActions}
                                filter={filter}
                                modelType={PermissionModel.customer}
                                detailsUrl={CUSTOMER_URLS.DETAILS}
                                EditContainer={CustomerUpsertForm}
                                ListContainer={CustomersTable}/>
    )
}


export default CustomersContainer;


