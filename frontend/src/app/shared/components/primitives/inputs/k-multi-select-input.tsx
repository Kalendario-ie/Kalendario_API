import React, {ChangeEvent} from 'react';
import {FormGroup} from 'reactstrap';
import {KBaseInputProps, MultiSelectOption} from 'src/app/shared/components/primitives/inputs/interfaces';
import { KCard, KTreeView } from '../containers';
import { KCheckbox } from './k-checkbox';

// @ts-ignore
interface KMultiSelectProps extends KBaseInputProps {
    name: string;
    value: number[];
    options: MultiSelectOption[];
}

export const KMultiSelectInput: React.FunctionComponent<KMultiSelectProps> = (
    {
        name,
        value,
        options,
        onChange,
        onBlur,
    }) => {
    const values = new Set<number>(value);

    const handleCheckboxChange = (option: MultiSelectOption) => (e: ChangeEvent<HTMLInputElement>) => {
        if (option.children && isOptionChecked(option)) {
            option.children.forEach(option => values.delete(option.id));
        } else if (option.children) {
            option.children.forEach(option => values.add(option.id));
        } else if (values.has(option.id)) {
            values.delete(option.id);
        } else {
            values.add(option.id);
        }
        onChange && onChange({...e, target: {...e.target, name, value: Array.from(values)}});
    }

    const isOptionChecked = (option: MultiSelectOption) => {
        return !option.children ? values.has(option.id) : option.children.every(option => values.has(option.id));
    }

    return (
        <KCard hasShadow={false}
               maxHeight={30}
               bodiless={true}
               mhUnit={'vh'}
        >
            <KTreeView items={options}
                       renderComponent={(option) =>
                           <FormGroup check>
                               <KCheckbox placeholder={option.name}
                                          name={name}
                                          onBlur={onBlur}
                                          onChange={handleCheckboxChange(option)}
                                          checked={isOptionChecked(option)}
                               />
                           </FormGroup>
                       }
            />
        </KCard>
    )
}
