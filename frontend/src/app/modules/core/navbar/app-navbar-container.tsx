import React, {useState} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {selectUser} from 'src/app/store/auth';
import {selectCartIsEmpty, selectCompany, selectCurrentRequest} from 'src/app/store/companies';
import {selectShowDashboardToggle, toggleDashboardSidenav} from 'src/app/store/ui';
import AppNavbar from './app-navbar';


const AppNavbarContainer: React.FunctionComponent = () => {
    const user = useSelector(selectUser);
    const [isOpen, setIsOpen] = useState(false);
    const toggleMenu = () => setIsOpen(!isOpen);
    const dispatch = useDispatch()
    const company = useSelector(selectCompany);
    const cart = useSelector(selectCurrentRequest);
    const cartIsEmpty = useSelector(selectCartIsEmpty);
    const showDashboardToggle = useSelector(selectShowDashboardToggle);
    const toggleSidenav = () => dispatch(toggleDashboardSidenav());

    return (
        <AppNavbar
            company={company}
            cart={cart}
            cartIsEmpty={cartIsEmpty}
            user={user}
            toggleMenu={toggleMenu}
            menuOpen={isOpen}
            showSidenavToggle={showDashboardToggle}
            toggleSidenav={toggleSidenav}
        />
    )
}


export default AppNavbarContainer;
