import React from 'react';
import {PermissionModel, PermissionType} from 'src/app/api/auth';
import {KIconButton} from 'src/app/shared/components/primitives/buttons';
import {useUserHasPermission} from 'src/app/shared/context-providers/auth-auto-login';

interface AdminButtonProps {
    type: PermissionType;
    model: PermissionModel;
    onClick: () => void;
}

function iconColor(type: PermissionType): string {
    switch (type) {
        case PermissionType.add:
            return 'primary';
        case PermissionType.change:
            return 'accent-light';
        case PermissionType.delete:
            return 'danger';
        case PermissionType.view:
            return 'primary';

    }
}

function iconType(type: PermissionType): string {
    switch (type) {
        case PermissionType.add:
            return 'plus';
        case PermissionType.change:
            return 'edit';
        case PermissionType.delete:
            return 'trash';
        case PermissionType.view:
            return 'external-link-alt';

    }
}

const AdminButton: React.FunctionComponent<AdminButtonProps> = (
    {
        type,
        model,
        onClick
    }) => {
    const hasPermission = useUserHasPermission(type, model);
    const icon = iconType(type);
    const color = iconColor(type)
    return (
        <>
            <KIconButton color={color}
                         icon={icon}
                         onClick={onClick}
                         disabled={!hasPermission}/>
        </>
    )
}


export default AdminButton;
