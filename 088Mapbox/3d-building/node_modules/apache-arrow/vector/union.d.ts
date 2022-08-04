import { BaseVector } from './base';
import { Union, DenseUnion, SparseUnion } from '../type';
/** @ignore */
export declare class UnionVector<T extends Union = Union> extends BaseVector<T> {
    get typeIdToChildIndex(): {
        [key: number]: number;
    };
}
/** @ignore */
export declare class DenseUnionVector extends UnionVector<DenseUnion> {
    get valueOffsets(): Int32Array;
}
/** @ignore */
export declare class SparseUnionVector extends UnionVector<SparseUnion> {
}
