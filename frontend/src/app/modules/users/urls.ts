import {pathWithParams} from 'src/app/shared/util/router-extensions';


export const USER_ROUTES = {
    ROOT: '/my',
    BOOKING: (date?: string) => pathWithParams('/my/bookings', {date})
}
