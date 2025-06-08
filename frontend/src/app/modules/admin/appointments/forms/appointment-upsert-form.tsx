import React, {useState} from 'react';
import {
    Appointment,
    CustomerAppointment,
    EventType,
    upsertCustomerAppointmentRequestParser,
    UpsertCustomerAppointmentRequestValidation,
    upsertEmployeeEventRequestParser,
    UpsertEmployeeEventRequestValidation
} from 'src/app/api/appointments';
import {PermissionModel} from 'src/app/api/auth';
import AppointmentHistoryContainer from 'src/app/modules/admin/appointments/appointment-history-container';
import DeleteButton from 'src/app/shared/admin/delete-button';
import {useInitializeEffect} from 'src/app/shared/admin/hooks';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import {KFlexRow} from 'src/app/shared/components/flex';
import {KFormikForm, KFormikInput} from 'src/app/shared/components/forms';
import KFormikDatetimeInput from 'src/app/shared/components/forms/k-formik-datetime-input';
import {KIconButton} from 'src/app/shared/components/primitives/buttons';
import {appointmentActions} from 'src/app/store/admin/appointments';
import {serviceActions} from 'src/app/store/admin/services';
import CustomerAppointmentUpsertForm from './customer-appointment-upsert-form';

const AppointmentUpsertForm: React.FunctionComponent<AdminEditContainerProps<Appointment>> = (
    {
        entity,
        apiError,
        onSubmit,
        onCancel
    }) => {
    const isAppointment = entity?.type === EventType.CustomerAppointment;
    const validationSchema = isAppointment ? UpsertCustomerAppointmentRequestValidation : UpsertEmployeeEventRequestValidation;
    const initialValues = isAppointment ? upsertCustomerAppointmentRequestParser(entity) : upsertEmployeeEventRequestParser(entity);
    const [showHistory, setShowHistory] = useState(false);
    useInitializeEffect(serviceActions);

    const handleHistoryClick = () => {
        setShowHistory(true);
    };

    const handleHistoryCloseClick = () => {
        setShowHistory(false);
    };

    return (
        <KFormikForm initialValues={initialValues}
                     apiError={apiError}
                     onSubmit={onSubmit}
                     onCancel={onCancel}
                     validationSchema={validationSchema}
        >
            {entity && entity.id !== 0 &&
            <KFlexRow justify="end">
                <DeleteButton entity={entity}
                              modelType={PermissionModel.appointment}
                              baseActions={appointmentActions}/>
                <KIconButton icon="history"
                             color="primary"
                             onClick={handleHistoryClick}/>
                <AppointmentHistoryContainer id={entity.id} isOpen={showHistory} onClose={handleHistoryCloseClick}/>
            </KFlexRow>
            }
            {isAppointment &&
            <CustomerAppointmentUpsertForm appointment={entity as CustomerAppointment}/>
            }
            {!isAppointment &&
            <>
                <KFormikDatetimeInput name="start"/>
                <KFormikDatetimeInput name="end"/>
                <KFormikInput name="internalNotes" as={'textarea'}/>
                <KFormikInput placeholder="Allow Overlapping" name="ignoreAvailability" as={'checkbox'}/>
            </>
            }
        </KFormikForm>
    )
}


export default AppointmentUpsertForm;
