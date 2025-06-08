export interface ApiBaseError {
  status: number;
  detail: any;
}


export interface ApiValidationError extends ApiBaseError {
    detail: {[key: string]: string[]};
}
