import React from "react"
import {Link} from "react-router-dom"
import {PermissionModel, PermissionType} from 'src/app/api/auth';
import KIcon from 'src/app/shared/components/primitives/k-icon';
import {useUserHasPermission} from 'src/app/shared/context-providers/auth-auto-login';
import {useKHistory} from 'src/app/shared/util/router-extensions';

export interface SideBarLinkItem {
    name: string;
    url: string;
    icon: string | undefined;
    permissionModel?: PermissionModel;
}

export interface SideBarLinks {
    [key: string]: SideBarLinkItem[]
}

interface KDashboardSidebarProps {
    links: SideBarLinks;
    isOpen: boolean;
}

export interface KDashboardSidebarLinkProps extends SideBarLinkItem {
    isOpen: boolean;
}


const KDashboardSidebarLink: React.FunctionComponent<KDashboardSidebarLinkProps> = (
    {
        isOpen,
        name,
        url,
        icon,
        permissionModel
    }) => {
    const {location: {pathname}} = useKHistory();
    const hasPermission = useUserHasPermission(PermissionType.view, permissionModel);

    return (
        <>
            {hasPermission &&
            <li className="sidebar-list-item" key={name}>
                <Link to={url}
                      className={`sidebar-link ${pathname === url ? ' active' : 'text-muted'}`}
                >
                    {icon && <KIcon icon={icon}/>}
                    {isOpen &&
                    name
                    }
                </Link>
            </li>
            }
        </>
    )
}

const KDashboardSidebar: React.FunctionComponent<KDashboardSidebarProps> = (
    {
        links,
        isOpen
    }) => {

    return (
        <div className={`sidebar ${isOpen ? 'open' : 'closed'} k-shadow-0 py-3`}>
            {Object.keys(links).map(key => {
                return (
                    <React.Fragment key={key}>
                        <h6 className="sidebar-heading">{key}</h6>
                        <ul className="list-clear">
                            {links[key].map(({name, url, icon, permissionModel}, k) =>
                                <KDashboardSidebarLink isOpen={isOpen}
                                                       key={k}
                                                       name={name}
                                                       url={url}
                                                       icon={icon}
                                                       permissionModel={permissionModel}/>
                            )}
                        </ul>
                    </React.Fragment>
                )
            })}
        </div>
    )
}


export default KDashboardSidebar;
