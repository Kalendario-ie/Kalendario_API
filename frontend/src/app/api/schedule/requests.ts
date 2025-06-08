export interface UpsertScheduleRequestFrame {
    start: string,
    end: string
}

export interface UpsertScheduleRequestShift {
    frames: UpsertScheduleRequestFrame[];
}

export interface UpsertScheduleRequest {
    name: string;
    mon: UpsertScheduleRequestShift;
    tue: UpsertScheduleRequestShift;
    wed: UpsertScheduleRequestShift;
    thu: UpsertScheduleRequestShift;
    fri: UpsertScheduleRequestShift;
    sat: UpsertScheduleRequestShift;
    sun: UpsertScheduleRequestShift;
}
