import * as moment from 'moment';
import {momentToIso} from 'src/app/shared/util/moment-helpers';

export function convertMoment(params: {[key: string]: any} = {}): any  {
  const result: {[key: string]: any} = {};
  Object.keys(params).forEach((prop: string) => {
    // @ts-ignore
    if (params[prop] instanceof moment) {
      result[prop] = momentToIso(params[prop]);
    } else {
      result[prop] = params[prop];
    }
  });
  return result;
}
