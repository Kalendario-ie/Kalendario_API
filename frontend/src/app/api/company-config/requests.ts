export interface UpsertCompanyConfigRequest {
    ownerId: number;
    private: boolean;
    preBookWarn: string;
    postBookMessage: string;
    postBookEmailMessage: string;
    appointmentReminderMessage: string;
    appointmentAcceptedMessage: string;
    appointmentRejectedMessage: string;
    allowCardPayment: boolean;
    allowUnpaidRequest: boolean;
}
