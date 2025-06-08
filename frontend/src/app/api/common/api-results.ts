export interface ApiListResult<R> {
  count: number;
  next: string;
  previous: string;
  results: R[];
}
