import moment, {Moment} from 'moment';


export const useTimeFormatter = () => {
    return (value: Moment | string) => moment.utc(value).format('DD/MM/YYYY HH:mm');
}
