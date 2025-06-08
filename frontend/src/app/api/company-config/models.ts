import {IReadModel} from "../common/models";

export interface CompanyConfig extends IReadModel {
    name: string;
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
    canReceiveCardPayments: boolean;
    canReceiveUnpaidRequest: boolean;
}
