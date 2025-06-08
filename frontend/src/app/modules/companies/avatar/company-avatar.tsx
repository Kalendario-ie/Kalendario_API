import React from 'react';
import {Company} from 'src/app/api/companies';
import { KFlexRow } from 'src/app/shared/components/flex';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';

interface CompanyAvatarProps {
    company: Company;
}

const CompanyAvatar: React.FunctionComponent<CompanyAvatarProps> = (
    {company}) => {
    return (
        <KFlexRow align="center">
            <AvatarImg src={company.avatar}/>
            <div className="ml-2">
                <h3 className="pb-0 c-pointer">{company.name}</h3>
                <div className="c-accent">
                    {company.address}
                </div>
            </div>
        </KFlexRow>
    );
}

export default CompanyAvatar;
