import React from 'react';
import {Button, Modal, ModalBody, ModalFooter, ModalHeader} from 'reactstrap';

export interface KModalButtonProps {
    text: string;
    color: 'primary' | 'secondary' | 'danger';
    onClick: () => void;
}

interface KModalProps {
    body: React.ReactNode;
    isOpen: boolean;
    header?: React.ReactNode;
    buttons?: KModalButtonProps[];
    backdrop?: boolean;
    scrollable?: boolean;
    onCancel?: () => void
}

const KModal: React.FunctionComponent<KModalProps> = (
    {
        header,
        body,
        buttons,
        backdrop = true,
        scrollable = true,
        isOpen,
        onCancel
    }) => {
    return (
        <Modal isOpen={isOpen}
               toggle={onCancel}
               backdrop={backdrop}
               scrollable={scrollable}
        >
            {header &&
            <ModalHeader toggle={onCancel}>
                {header}
            </ModalHeader>
            }
            <ModalBody className={"m-2"}>
                {body}
            </ModalBody>
            {buttons &&
            <ModalFooter>
                {buttons.map((button, key) =>
                    <Button key={key}
                            color={button.color}
                            onClick={button.onClick}
                    >
                        {button.text}</Button>)}
            </ModalFooter>
            }
        </Modal>
    )
}


export default KModal;
