import { DataType } from './type';
export declare class Schema<T extends {
    [key: string]: DataType;
} = any> {
    readonly fields: Field<T[keyof T]>[];
    readonly metadata: Map<string, string>;
    readonly dictionaries: Map<number, DataType>;
    constructor(fields?: Field[], metadata?: Map<string, string> | null, dictionaries?: Map<number, DataType> | null);
    get [Symbol.toStringTag](): string;
    toString(): string;
    select<K extends keyof T = any>(...columnNames: K[]): Schema<{ [P in K]: T[P]; }>;
    selectAt<K extends T[keyof T] = any>(...columnIndices: number[]): Schema<{
        [key: string]: K;
    }>;
    assign<R extends {
        [key: string]: DataType;
    } = any>(schema: Schema<R>): Schema<T & R>;
    assign<R extends {
        [key: string]: DataType;
    } = any>(...fields: (Field<R[keyof R]> | Field<R[keyof R]>[])[]): Schema<T & R>;
}
export declare class Field<T extends DataType = any> {
    static new<T extends DataType = any>(props: {
        name: string | number;
        type: T;
        nullable?: boolean;
        metadata?: Map<string, string> | null;
    }): Field<T>;
    static new<T extends DataType = any>(name: string | number | Field<T>, type: T, nullable?: boolean, metadata?: Map<string, string> | null): Field<T>;
    readonly type: T;
    readonly name: string;
    readonly nullable: boolean;
    readonly metadata: Map<string, string>;
    constructor(name: string, type: T, nullable?: boolean, metadata?: Map<string, string> | null);
    get typeId(): import("./enum").Type;
    get [Symbol.toStringTag](): string;
    toString(): string;
    clone<R extends DataType = T>(props: {
        name?: string | number;
        type?: R;
        nullable?: boolean;
        metadata?: Map<string, string> | null;
    }): Field<R>;
    clone<R extends DataType = T>(name?: string | number | Field<T>, type?: R, nullable?: boolean, metadata?: Map<string, string> | null): Field<R>;
}
