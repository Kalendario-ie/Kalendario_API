import React, {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import KDashboardContent from 'src/app/shared/components/dashboard/k-dashboard-content';
import KDashboardSidebar, {SideBarLinks} from 'src/app/shared/components/dashboard/k-dashboard-sidebar';
import {KFlexRow} from 'src/app/shared/components/flex';
import {selectSidenavOpen, setShowDashboardToggle} from 'src/app/store/ui';

interface DashboardContainerProps {
    links: SideBarLinks;
    children?: React.ReactNode;
}

const KDashboardContainer: React.FunctionComponent<DashboardContainerProps> = (
    {
        links,
        children
    }) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(setShowDashboardToggle(true));
        return () => {
            dispatch(setShowDashboardToggle(false));
        };
    }, [dispatch]);

    const isOpen = useSelector(selectSidenavOpen);

    return (
        <KFlexRow align={'stretch'}>
            <KDashboardSidebar
                links={links}
                isOpen={isOpen}
            />
            <KDashboardContent>
                {children}
            </KDashboardContent>
        </KFlexRow>
    )
}


export default KDashboardContainer;
