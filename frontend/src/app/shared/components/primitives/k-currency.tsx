import React from 'react';

interface CurrencyProps {
    value: number;
}

export const KCurrency: React.FunctionComponent<CurrencyProps> = (
    {
        value
    }) => {
    return (
        <>{value.toFixed(2)} €</>
    )
}
