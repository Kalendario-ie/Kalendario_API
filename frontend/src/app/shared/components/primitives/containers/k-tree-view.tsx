import React, {useState} from 'react';
import {TreeViewItem} from '.';
import {KFlexRow} from '../../flex';
import {KIconButton} from '../buttons';


interface KTreeViewProps {
    items: TreeViewItem[];
    renderComponent: React.FunctionComponent<TreeViewItem>;
}

export const KTreeView: React.FunctionComponent<KTreeViewProps> = (
    {
        items,
        renderComponent
    }) => {
    const [openOptions, setOpenOptions] = useState(new Set<number>());

    const openCloseDrawer = (id: number) => {
        openOptions.has(id) ? openOptions.delete(id) : openOptions.add(id);
        setOpenOptions(new Set(openOptions));
    }

    return (
        <ul className="tree-view ul-none">
            {items.map(option =>
                <li key={option.id}>
                    <KFlexRow>
                        {option.children &&
                        <KIconButton onClick={() => openCloseDrawer(option.id)} icon={'caret-right'}/>
                        }
                        {renderComponent(option)}
                    </KFlexRow>
                    {option.children && openOptions.has(option.id) &&
                    <KTreeView renderComponent={renderComponent} items={option.children}/>
                    }
                </li>
            )}
        </ul>
    )
}
