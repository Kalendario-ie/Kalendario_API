import React, {useState} from 'react';
import {Tooltip} from 'reactstrap';

interface KTooltipProps {
    id: string;
    text: string;
}

const KTooltip: React.FunctionComponent<KTooltipProps> = (
    {
        id,
        text
    }) => {
    const [tooltipOpen, setTooltipOpen] = useState(false);
    const toggle = () => setTooltipOpen(!tooltipOpen);

    return (
        <Tooltip placement="right" target={id} isOpen={tooltipOpen} toggle={toggle}>
            {text}
        </Tooltip>
    )
}


export default KTooltip;
