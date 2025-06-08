import {ApiValidationError} from 'src/app/api/common/api-errors';
import { IReadModel } from "src/app/api/common/models";

export interface AdminEditContainerProps<TEntity> {
    entity: TEntity | null;
    apiError: ApiValidationError | null;
    onSubmit: (values: any) => void;
    onCancel: () => void;
}

export interface AdminTableContainerProps<TModel> {
    entities: TModel[];
    filter?: (value: string | undefined) => void;
    buttonsColumn: any
}
