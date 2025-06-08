import React from 'react';
import {useDispatch, useSelector} from 'react-redux';
import CompaniesView from 'src/app/modules/companies/companies-view';
import SlotsForServiceModal from 'src/app/modules/companies/company-services/slots-for-service-modal';
import {selectCompany, selectService, setSelectedServiceId} from 'src/app/store/companies';

interface CompaniesMainProps {
}

const CompaniesContainer: React.FunctionComponent<CompaniesMainProps>  = () => {
    const dispatch = useDispatch();
    const company = useSelector(selectCompany);
    const service = useSelector(selectService);

    const serviceClick = (id: number | null) => {
        dispatch(setSelectedServiceId(id));
    }

    return (
        <>
            {company &&
            <CompaniesView company={company} serviceClick={serviceClick}/>
            }
            <SlotsForServiceModal service={service} onCancel={() => serviceClick(null)}/>
        </>
    )
}


export default CompaniesContainer;
