import React from 'react';
import AsyncSelect from 'react-select/async';
import {Company} from 'src/app/api/companies';
import {KFlexRow} from 'src/app/shared/components/flex';
import {KPageContainer} from 'src/app/shared/components/primitives/containers';


interface HomeViewProps {
    values: (value: string) => Promise<Company[]>,
    onChange: (value: Company | null) => void;
}

const HomeView: React.FunctionComponent<HomeViewProps> = (
    {
        values,
        onChange
    }) => {

    const groupStyles = {
        width: '400px',
    };

    return (
        <KPageContainer>
            <KFlexRow justify="center">
                <div style={groupStyles} className="company-shadow-1">
                    <AsyncSelect cacheOptions
                                 defaultOptions
                                 backspaceRemovesValue
                                 getOptionValue={(option) => option.name}
                                 getOptionLabel={(option) => option.name}
                                 onChange={(value, bc) => onChange(value)}
                                 loadOptions={values}/>
                </div>
            </KFlexRow>
        </KPageContainer>
    )
}

export default HomeView;
