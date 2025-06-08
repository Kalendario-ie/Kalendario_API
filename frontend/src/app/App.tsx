import React from 'react';
import AppNavbarContainer from 'src/app/modules/core/navbar/app-navbar-container';
import AppRoutes from './app-routes';
import AppIntl from './AppIntl';


function App() {
    return (
        <AppIntl language={'en'}>
            <AppNavbarContainer/>
            <AppRoutes/>
        </AppIntl>
    );
}

export default App;
