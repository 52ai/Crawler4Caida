import { flatbuffers } from 'flatbuffers';
import ByteBuffer = flatbuffers.ByteBuffer;
import { TypedArray, TypedArrayConstructor } from '../interfaces';
import { BigIntArray, BigIntArrayConstructor } from '../interfaces';
/** @ignore */
export declare function memcpy<TTarget extends ArrayBufferView, TSource extends ArrayBufferView>(target: TTarget, source: TSource, targetByteOffset?: number, sourceByteLength?: number): TTarget;
/** @ignore */
export declare function joinUint8Arrays(chunks: Uint8Array[], size?: number | null): [Uint8Array, Uint8Array[], number];
/** @ignore */
export declare type ArrayBufferViewInput = ArrayBufferView | ArrayBufferLike | ArrayBufferView | Iterable<number> | ArrayLike<number> | ByteBuffer | string | null | undefined | IteratorResult<ArrayBufferView | ArrayBufferLike | ArrayBufferView | Iterable<number> | ArrayLike<number> | ByteBuffer | string | null | undefined> | ReadableStreamReadResult<ArrayBufferView | ArrayBufferLike | ArrayBufferView | Iterable<number> | ArrayLike<number> | ByteBuffer | string | null | undefined>;
/** @ignore */
export declare function toArrayBufferView<T extends TypedArray>(ArrayBufferViewCtor: TypedArrayConstructor<T>, input: ArrayBufferViewInput): T;
export declare function toArrayBufferView<T extends BigIntArray>(ArrayBufferViewCtor: BigIntArrayConstructor<T>, input: ArrayBufferViewInput): T;
/** @ignore */ export declare const toInt8Array: (input: ArrayBufferViewInput) => Int8Array;
/** @ignore */ export declare const toInt16Array: (input: ArrayBufferViewInput) => Int16Array;
/** @ignore */ export declare const toInt32Array: (input: ArrayBufferViewInput) => Int32Array;
/** @ignore */ export declare const toBigInt64Array: (input: ArrayBufferViewInput) => BigInt64Array;
/** @ignore */ export declare const toUint8Array: (input: ArrayBufferViewInput) => Uint8Array;
/** @ignore */ export declare const toUint16Array: (input: ArrayBufferViewInput) => Uint16Array;
/** @ignore */ export declare const toUint32Array: (input: ArrayBufferViewInput) => Uint32Array;
/** @ignore */ export declare const toBigUint64Array: (input: ArrayBufferViewInput) => BigUint64Array;
/** @ignore */ export declare const toFloat32Array: (input: ArrayBufferViewInput) => Float32Array;
/** @ignore */ export declare const toFloat64Array: (input: ArrayBufferViewInput) => Float64Array;
/** @ignore */ export declare const toUint8ClampedArray: (input: ArrayBufferViewInput) => Uint8ClampedArray;
/** @ignore */
declare type ArrayBufferViewIteratorInput = Iterable<ArrayBufferViewInput> | ArrayBufferViewInput;
/** @ignore */
export declare function toArrayBufferViewIterator<T extends TypedArray>(ArrayCtor: TypedArrayConstructor<T>, source: ArrayBufferViewIteratorInput): Generator<T, T, number | undefined>;
/** @ignore */ export declare const toInt8ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Int8Array, Int8Array, number | undefined>;
/** @ignore */ export declare const toInt16ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Int16Array, Int16Array, number | undefined>;
/** @ignore */ export declare const toInt32ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Int32Array, Int32Array, number | undefined>;
/** @ignore */ export declare const toUint8ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Uint8Array, Uint8Array, number | undefined>;
/** @ignore */ export declare const toUint16ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Uint16Array, Uint16Array, number | undefined>;
/** @ignore */ export declare const toUint32ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Uint32Array, Uint32Array, number | undefined>;
/** @ignore */ export declare const toFloat32ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Float32Array, Float32Array, number | undefined>;
/** @ignore */ export declare const toFloat64ArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Float64Array, Float64Array, number | undefined>;
/** @ignore */ export declare const toUint8ClampedArrayIterator: (input: ArrayBufferViewIteratorInput) => Generator<Uint8ClampedArray, Uint8ClampedArray, number | undefined>;
/** @ignore */
declare type ArrayBufferViewAsyncIteratorInput = AsyncIterable<ArrayBufferViewInput> | Iterable<ArrayBufferViewInput> | PromiseLike<ArrayBufferViewInput> | ArrayBufferViewInput;
/** @ignore */
export declare function toArrayBufferViewAsyncIterator<T extends TypedArray>(ArrayCtor: TypedArrayConstructor<T>, source: ArrayBufferViewAsyncIteratorInput): AsyncGenerator<T, T, number | undefined>;
/** @ignore */ export declare const toInt8ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Int8Array, Int8Array, number | undefined>;
/** @ignore */ export declare const toInt16ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Int16Array, Int16Array, number | undefined>;
/** @ignore */ export declare const toInt32ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Int32Array, Int32Array, number | undefined>;
/** @ignore */ export declare const toUint8ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Uint8Array, Uint8Array, number | undefined>;
/** @ignore */ export declare const toUint16ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Uint16Array, Uint16Array, number | undefined>;
/** @ignore */ export declare const toUint32ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Uint32Array, Uint32Array, number | undefined>;
/** @ignore */ export declare const toFloat32ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Float32Array, Float32Array, number | undefined>;
/** @ignore */ export declare const toFloat64ArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Float64Array, Float64Array, number | undefined>;
/** @ignore */ export declare const toUint8ClampedArrayAsyncIterator: (input: ArrayBufferViewAsyncIteratorInput) => AsyncGenerator<Uint8ClampedArray, Uint8ClampedArray, number | undefined>;
/** @ignore */
export declare function rebaseValueOffsets(offset: number, length: number, valueOffsets: Int32Array): Int32Array;
/** @ignore */
export declare function compareArrayLike<T extends ArrayLike<any>>(a: T, b: T): boolean;
export {};
