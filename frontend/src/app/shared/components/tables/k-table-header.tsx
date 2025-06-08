import React from 'react';
import {HeaderGroup} from 'react-table';

interface KTableHeaderProps<D extends object> {
    headerGroups: Array<HeaderGroup<D>>;
}

function KTableHeader<D extends object>({headerGroups}: KTableHeaderProps<D>) {
    return (
        <thead>
        {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                    <th {...column.getHeaderProps()}>
                        {column.render('Header')}
                        {/* Render the columns filter UI */}
                        <div>
                            {
                                // @ts-ignore
                                column.canFilter ? column.render('Filter') : null
                            }
                        </div>
                    </th>
                ))}
            </tr>
        ))}
        </thead>
    )
}


export default KTableHeader;
