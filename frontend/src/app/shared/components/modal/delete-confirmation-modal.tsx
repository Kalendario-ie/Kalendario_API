import React, {useState} from 'react';
import {FormattedMessage} from 'react-intl';
import {AnyAction} from 'redux';
import KModal, {KModalButtonProps} from 'src/app/shared/components/modal/k-modal';
import {useAppDispatch} from 'src/app/store';

interface ConfirmationModalProps {
    messageId?: string;
    isOpen: boolean;
    onConfirm: () => void;
    onCancel: () => void;
}

const DeleteConfirmationModal: React.FunctionComponent<ConfirmationModalProps> = (
    {
        messageId = "COMMON.SURE-DELETE",
        isOpen,
        onCancel,
        onConfirm

    }) => {

    const buttons: KModalButtonProps[] = [
        {
            text: 'confirm',
            color: 'primary',
            onClick: onConfirm
        },
        {
            text: 'cancel',
            color: 'danger',
            onClick: onCancel
        }
    ]

    return (
        <KModal
            body={<FormattedMessage id={messageId}/>}
            isOpen={isOpen}
            buttons={buttons}
        />
    )
}


export function useConfirmationModal(onConfirm: (id: number) => void): [(id: number) => void, JSX.Element] {
    const [id, setId] = useState<number | null>(null);

    const handleConfirm = () => {
        onConfirm(id!);
        setId(null);
    }

    const handleCancel = () => {
        setId(null);
    }

    const modal = <DeleteConfirmationModal isOpen={!!id}
                                           onConfirm={handleConfirm}
                                           onCancel={handleCancel}/>

    return [setId, modal]
}

export function UseConfirmationModalWithDispatch(onConfirm: (id: number) => AnyAction): [(id: number) => void, JSX.Element] {
    const dispatch = useAppDispatch();
    const handleConfirmClick = (id: number) => dispatch(onConfirm(id));
    return useConfirmationModal(handleConfirmClick);
}

export default DeleteConfirmationModal;
