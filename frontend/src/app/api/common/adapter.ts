export interface Adapter<T> {
  adapt(item: any): T;
}

export function adaptList<T>(adapter: (item: any) => T) {
  return (data: any[]) => data.map(item => adapter(item));
}

