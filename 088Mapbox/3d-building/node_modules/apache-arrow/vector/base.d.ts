import { Data } from '../data';
import { DataType } from '../type';
import { Chunked } from './chunked';
import { VectorType as V } from '../interfaces';
import { AbstractVector, Vector, Clonable, Sliceable, Applicative } from '../vector';
/** @ignore */
export interface BaseVector<T extends DataType = any> extends Clonable<V<T>>, Sliceable<V<T>>, Applicative<T, Chunked<T>> {
    slice(begin?: number, end?: number): V<T>;
    concat(...others: Vector<T>[]): Chunked<T>;
    clone<R extends DataType = T>(data: Data<R>, children?: Vector<R>[]): V<R>;
}
/** @ignore */
export declare abstract class BaseVector<T extends DataType = any> extends AbstractVector<T> implements Clonable<V<T>>, Sliceable<V<T>>, Applicative<T, Chunked<T>> {
    protected _children?: Vector[];
    constructor(data: Data<T>, children?: Vector[]);
    readonly data: Data<T>;
    readonly numChildren: number;
    get type(): T;
    get typeId(): T["TType"];
    get length(): number;
    get offset(): number;
    get stride(): number;
    get nullCount(): number;
    get byteLength(): number;
    get VectorName(): string;
    get ArrayType(): T['ArrayType'];
    get values(): T["TArray"];
    get typeIds(): T["TArray"];
    get nullBitmap(): Uint8Array;
    get valueOffsets(): Int32Array;
    get [Symbol.toStringTag](): string;
    isValid(index: number): boolean;
    getChildAt<R extends DataType = any>(index: number): Vector<R> | null;
    toJSON(): any;
    protected _sliceInternal(self: this, begin: number, end: number): any;
    protected _bindDataAccessors(data: Data<T>): void;
}
