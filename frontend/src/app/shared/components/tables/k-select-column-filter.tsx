import React from 'react';
import {KInput} from 'src/app/shared/components/primitives/inputs';

interface FilterOption {
    id: number | string;
    name: string | number;
}

interface KSelectColumnFilterProps {
    column: {
        filterValue: string;
        setFilter: (value: string | undefined) => void;
        preFilteredRows: any[];
        id: any;
    },
    options?: FilterOption[];
}

export const KSelectColumnFilter: React.FunctionComponent<KSelectColumnFilterProps> = (
    {
        column: {
            filterValue,
            setFilter,
            preFilteredRows,
            id
        },
        options
    }) => {

    const rowOptions = React.useMemo(() => {
        const options = new Set<number | string>()
        preFilteredRows.forEach(row => {
            options.add(row.values[id])
        })
        return Array.from(options).map(opt => ({id: opt, name: opt}));
    }, [id, preFilteredRows])

    const usedOptions = options || rowOptions;

    return (
        <KInput
            type="select"
            value={filterValue}
            onChange={e => setFilter(e?.target.value || undefined)}
        >
            <option value="">All</option>
            {usedOptions.map((option, i) => (
                <option key={i} value={option.id}>
                    {option.name}
                </option>
            ))}
        </KInput>
    )
}
