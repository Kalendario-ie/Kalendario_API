import React from 'react';
import {isMobile} from 'react-device-detect';
import {Service, ServiceCategory} from 'src/app/api/services/models';
import CompanyServicesItem from 'src/app/modules/companies/company-services/company-services-item';
import {KFlexRow, KFlexRowItem} from 'src/app/shared/components/flex';
import KGrid from 'src/app/shared/components/grid/k-grid';
import {KCard} from 'src/app/shared/components/primitives/containers';

interface CompanyServicesListProps {
    services: Service[];
    categories: ServiceCategory[];
    serviceClick: (id: number) => void;
}

const CompanyServicesList: React.FunctionComponent<CompanyServicesListProps> = (
    {
        services,
        categories,
        serviceClick
    }) => {
    return (
        <KCard>
            <KFlexRow>
                {categories?.length > 1 &&
                <KFlexRowItem>
                    {categories.map((c, k) => <div key={k}>{c.name}</div>)}
                </KFlexRowItem>
                }
                <KFlexRowItem grow={4}>
                    <KGrid size={isMobile ? 12 : 6}>
                        {services?.map((s, k) => <CompanyServicesItem key={k}
                                                                      onClick={serviceClick}
                                                                      service={s}/>)}
                    </KGrid>
                </KFlexRowItem>
            </KFlexRow>
        </KCard>
    )
}

export default CompanyServicesList;
