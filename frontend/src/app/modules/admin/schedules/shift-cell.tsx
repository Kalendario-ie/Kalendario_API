import React from 'react';
import {Shift} from 'src/app/api/shifts';
import {KFlexColumn} from 'src/app/shared/components/flex';

interface ShiftCellProps {
    shift: Shift;
}

const ShiftCell: React.FunctionComponent<ShiftCellProps> = (
    {
        shift
    }) => {
    return (
        <KFlexColumn>
            {shift.frames.map((frame, key) => <div key={key}>{frame.name}</div>)}
        </KFlexColumn>
    )
}


export default ShiftCell;
