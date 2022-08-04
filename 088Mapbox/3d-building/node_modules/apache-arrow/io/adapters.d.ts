/// <reference types="node" />
import { ArrayBufferViewInput } from '../util/buffer';
import { ReadableDOMStreamOptions } from './interfaces';
declare type Uint8ArrayGenerator = Generator<Uint8Array, null, {
    cmd: 'peek' | 'read';
    size: number;
}>;
declare type AsyncUint8ArrayGenerator = AsyncGenerator<Uint8Array, null, {
    cmd: 'peek' | 'read';
    size: number;
}>;
declare const _default: {
    fromIterable<T extends ArrayBufferViewInput>(source: T | Iterable<T>): Uint8ArrayGenerator;
    fromAsyncIterable<T_1 extends ArrayBufferViewInput>(source: AsyncIterable<T_1> | PromiseLike<T_1>): AsyncUint8ArrayGenerator;
    fromDOMStream<T_2 extends ArrayBufferViewInput>(source: ReadableStream<T_2>): AsyncUint8ArrayGenerator;
    fromNodeStream(stream: NodeJS.ReadableStream): AsyncUint8ArrayGenerator;
    toDOMStream<T_3>(source: Iterable<T_3> | AsyncIterable<T_3>, options?: ReadableDOMStreamOptions | undefined): ReadableStream<T_3>;
    toNodeStream<T_4>(source: Iterable<T_4> | AsyncIterable<T_4>, options?: import("stream").ReadableOptions | undefined): import('stream').Readable;
};
/** @ignore */
export default _default;
