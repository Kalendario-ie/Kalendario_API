import React, {useEffect, useState} from 'react';
import {IReadModel} from 'src/app/api/common/models';
import {AdminEditContainerProps} from 'src/app/shared/admin/interfaces';
import KModal from 'src/app/shared/components/modal/k-modal';
import {useAppDispatch, useAppSelector} from 'src/app/store';
import {BaseActions, BaseSelectors} from 'src/app/store/admin/common/adapter';

export function useEditModal<TEntity extends IReadModel>(
    baseSelectors: BaseSelectors<TEntity>,
    baseActions: BaseActions,
    EditContainer: React.FunctionComponent<AdminEditContainerProps<TEntity>>
): [(entity: TEntity | null) => () => void, JSX.Element, TEntity | undefined] {
    const [selectedEntity, setSelectedEntity] = useState<TEntity | null>(null);
    const apiError = useAppSelector(baseSelectors.selectApiError);
    const editMode = useAppSelector(baseSelectors.selectEditMode);
    const createdEntity = useAppSelector(baseSelectors.selectCreatedEntity)
    const dispatch = useAppDispatch();

    const handleEditCancel = () => {
        setSelectedEntity(null);
        dispatch(baseActions.setEditMode(false));
    }

    const handleSubmit = (entity: any) => {
        if (!selectedEntity || selectedEntity.id === 0) {
            dispatch(baseActions.createEntity({entity}));
        } else {
            dispatch(baseActions.patchEntity({id: selectedEntity.id, entity}));
        }
    }

    const openModal = React.useMemo(() =>
        (entity: TEntity | null) => () => {
            setSelectedEntity(entity);
            dispatch(baseActions.setEditMode(true));
        }, [baseActions, dispatch])

    const modal = <KModal body={<EditContainer entity={selectedEntity}
                                               apiError={apiError}
                                               onSubmit={handleSubmit}
                                               onCancel={handleEditCancel}/>}
                          isOpen={editMode}/>

    return [openModal, modal, createdEntity]
}


export function useSelectAll<TEntity>(baseSelectors: BaseSelectors<TEntity>, baseActions: BaseActions) {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(baseActions.initializeStore());
    }, [baseActions, dispatch]);
    return useAppSelector(baseSelectors.selectAll);
}

/**
 * a shortcut effect to dispatch the initialize store action
 * @param baseActions The base action for the store that needs to be initialized
 */
export function useInitializeEffect(baseActions: BaseActions) {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(baseActions.initializeStore());
    }, [baseActions, dispatch]);
}
