import React, {useEffect, useState} from 'react';
import {IntlProvider} from 'react-intl';

function loadLocaleData(locale: string) {
    switch (locale) {
        default:
            return import('src/i18n/locale-data/en.json')
    }
}

function flattenMessages(object: object, prefix: string = '') {
    return Object.keys(object).reduce((messages, key) => {
        // @ts-ignore
        const value = object[key];
       const prefixedKey = prefix ? `${prefix}.${key}` : key;
       if (typeof value == 'string') {
           // @ts-ignore
           messages[prefixedKey] = value;
       } else {
           Object.assign(messages, flattenMessages(value, prefixedKey));
       }
       return messages;
    }, {});
}

interface AppItlProps {
    language: string;
    children: React.ReactChild | React.ReactChild[];
}

const AppIntl: React.FunctionComponent<AppItlProps> = ({language, children}) => {
    const [messages, setMessages] = useState({});
    useEffect(() => {
        loadLocaleData(language).then(m => {
            const flattenedMessages = flattenMessages(m.default);
            setMessages(flattenedMessages)
            }
        );
    }, [language])
    return (
        <IntlProvider
            messages={messages}
            locale="en"
            defaultLocale="en"
        >
            {children}
        </IntlProvider>
    )
}

export default AppIntl;
