import React, {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {Redirect} from 'react-router-dom';
import {CreateAppointmentRequest} from 'src/app/api/companies';
import {companiesUrls} from 'src/app/modules/companies/paths';
import {useQueryParams} from 'src/app/shared/util/router-extensions';
import {bookSlotRequest, selectCompany} from 'src/app/store/companies';


const BookContainer: React.FunctionComponent = () => {
    const {service, start, employee} = useQueryParams();
    const company = useSelector(selectCompany);
    const dispatch = useDispatch();
    useEffect(() => {
        if (company) {
            const request: CreateAppointmentRequest = {start, service: +service};
            if (employee) request.employee = +employee;
            dispatch(bookSlotRequest(request))
        }
    }, [company, dispatch, employee, service, start]);
    return (
        <>
            {company &&
            <Redirect to={companiesUrls(company).cart}/>
            }
        </>
    )
}


export default BookContainer;
