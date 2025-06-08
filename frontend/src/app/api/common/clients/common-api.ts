import {AxiosInstance, AxiosRequestConfig} from 'axios';
import {authApi} from 'src/app/api/auth';
import {getToken, removeToken} from '../session-storage';
import {ApiBaseError} from '../api-errors';


export const setupAuthHandlers = (apiAxios: AxiosInstance) => {
    const onRequestSuccess = (config: AxiosRequestConfig) => {
        const token = getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config
    }

    const onResponseError = async (error: any) => {
        let {status, headers, config, data} = error.response;

        if (status === 401) {
            if (config.url === 'auth/token/refresh/') {
                removeToken();
                return Promise.reject(error);
            }
            if (!config._retry) {
                config._retry = true;
                return authApi.refreshAccessToken(apiAxios)
                    .then(access_token => {
                        if (access_token) {
                            apiAxios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
                            return apiAxios(config);
                        }
                    });
            }
        }
        // Create Api Validation Response
        if (status === 422) {
            return Promise.reject<ApiBaseError>({status, detail: data.detail});
        }
        const applicationError = headers['applicationError'];
        if (applicationError) {
            return Promise.reject(applicationError);
        }
        let modalStateErrors = '';
        if (data && typeof data === 'object') {
            for (const key in Object.keys(data)) {
                if (data[key]) {
                    if (key !== 'message' && key !== 'detail') {
                        modalStateErrors += `${key}:`;
                    }
                    modalStateErrors += `${data[key]}\n`;
                }
            }
        }
        return Promise.reject(modalStateErrors || data || 'Server Error');
    }

    apiAxios.interceptors.request.use(onRequestSuccess, error => Promise.reject(error));
    apiAxios.interceptors.response.use((response) => response, onResponseError);
}


