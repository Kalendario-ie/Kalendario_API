import React from 'react';
import {RouteComponentProps} from 'react-router';
import {Redirect, Route, useHistory, useLocation} from 'react-router-dom';
import Spinner from 'reactstrap/es/Spinner';
import {PermissionModel, PermissionType} from 'src/app/api/auth';
import {AUTH_ROUTES} from 'src/app/modules/auth/urls';
import {KFlexRow} from 'src/app/shared/components/flex';
import {useCurrentUser, useUserHasPermission} from 'src/app/shared/context-providers/auth-auto-login';


export type QueryParams = Record<string, string | number | undefined>;

export function useQueryParams(): { [key: string]: string } {
    const params = new URLSearchParams(useLocation().search);
    const result: { [key: string]: string } = {};
    params.forEach(((value, key) => result[key] = value));
    return result;
}

export function useKHistory() {
    const history = useHistory();
    const push = (value: string, params?: QueryParams) => history.push(pathWithParams(value, params));
    return {...history, push}
}


interface ProtectedRouteProps {
    path: string;
    component: React.ComponentType<RouteComponentProps<any>> | React.ComponentType<any>;
    permissionModel?: PermissionModel;
    permissionType?: PermissionType;
}

export const ProtectedRoute: React.FunctionComponent<ProtectedRouteProps> = (
    {
        path,
        component,
        permissionModel,
        permissionType = PermissionType.view,
    }) => {
    const {returnUrl, ...params} = useQueryParams();
    const {location: {pathname}} = useKHistory();
    const [loading, user] = useCurrentUser();
    const hasPermission = useUserHasPermission(permissionType, permissionModel);

    return (
        <>
            {loading &&
            <KFlexRow className="h-100vh" align={'center'} justify={'center'}>
                Loading
                <Spinner className={"ml-2"} color="primary"/>
            </KFlexRow>
            }
            {!loading &&
            <>
                {user && hasPermission &&
                <Route path={path} component={component}/>
                }
                {user && !hasPermission &&
                <>
                    unauthorized access
                </>
                }
                {!user &&
                <Redirect to={pathWithParams(AUTH_ROUTES.LOGIN, {...params, returnUrl: pathname})}/>
                }
            </>
            }
        </>
    )
}


export function pathWithParams(path: string, queryParams: QueryParams | null | undefined): string {
    return `${path}${queryParams ? '?' + createQueryString(queryParams) : ''}`;
}

function createQueryString(params?: QueryParams): string {
    if (!params) return '';
    const url = Object.keys(params).map(key => `${key}=${params[key]}`).join('&');
    return encodeURI(url);
}
