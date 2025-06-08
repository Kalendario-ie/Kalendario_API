import axios, {AxiosResponse} from 'axios';
import {ApiListResult} from '../api-results';
import {convertMoment} from '../helpers';
import baseApiAxios from './base-api';

export interface BaseModelRequest<TEntity, TFilter  = object> {
    get: (filter: TFilter) => Promise<ApiListResult<TEntity>>;
    post: (model: any) => Promise<TEntity>;
    detail: (id: number, params?: {}) => Promise<TEntity>;
    patch: (id: number, model: any) => Promise<TEntity>;
    put(id: number, model: any): Promise<TEntity>;
    delete: (id: number) => Promise<AxiosResponse>;
}

function baseModelRequest<TEntity, TFilter = object>(baseUrl: string, adapter: (model: any) => TEntity): BaseModelRequest<TEntity, TFilter> {
    const token = axios.CancelToken;
    let source = token.source();
    return {
        get(filter: any): Promise<ApiListResult<TEntity>> {
            const params = convertMoment(filter);
            source.cancel('New request was made, canceling old request.');
            source = token.source();
            return baseApiAxios.get<ApiListResult<TEntity>>(baseUrl, {params, cancelToken: source.token})
                .then(project => {
                        project.data.results = project.data.results.map(r => adapter(r));
                        return project.data;
                    }
                )
        },

        post(model: any): Promise<TEntity> {
            return baseApiAxios.post(baseUrl, model)
                .then(result => adapter(result.data));
        },

        detail(id: number, params = {}): Promise<TEntity> {
            return baseApiAxios.get<TEntity>(baseUrl + id + '/', {params: {...params}})
                .then(result => adapter(result.data));
        },

        patch(id: number, model: any): Promise<TEntity> {
            return baseApiAxios.patch<TEntity>(baseUrl + id + '/', model)
                .then(result => adapter(result.data));
        },

        put(id: number, model: any): Promise<TEntity> {
            return baseApiAxios.put<TEntity>(baseUrl + id + '/', model)
                .then(result => adapter(result.data));
        },

        delete(id: number): Promise<AxiosResponse> {
            return baseApiAxios.delete<void>(baseUrl + id + '/');
        }
    }

}

export default baseModelRequest;
