import { flatbuffers } from 'flatbuffers';
/**
 * Logical types, vector layouts, and schemas
 *
 * @enum {number}
 */
export declare enum MetadataVersion {
    /**
     * 0.1.0 (October 2016).
     */
    V1 = 0,
    /**
     * 0.2.0 (February 2017). Non-backwards compatible with V1.
     */
    V2 = 1,
    /**
     * 0.3.0 -> 0.7.1 (May - December 2017). Non-backwards compatible with V2.
     */
    V3 = 2,
    /**
     * >= 0.8.0 (December 2017). Non-backwards compatible with V3.
     */
    V4 = 3,
    /**
     * >= 1.0.0 (July 2020. Backwards compatible with V4 (V5 readers can read V4
     * metadata and IPC messages). Implementations are recommended to provide a
     * V4 compatibility mode with V5 format changes disabled.
     *
     * Incompatible changes between V4 and V5:
     * - Union buffer layout has changed. In V5, Unions don't have a validity
     *   bitmap buffer.
     */
    V5 = 4
}
/**
 * Represents Arrow Features that might not have full support
 * within implementations. This is intended to be used in
 * two scenarios:
 *  1.  A mechanism for readers of Arrow Streams
 *      and files to understand that the stream or file makes
 *      use of a feature that isn't supported or unknown to
 *      the implementation (and therefore can meet the Arrow
 *      forward compatibility guarantees).
 *  2.  A means of negotiating between a client and server
 *      what features a stream is allowed to use. The enums
 *      values here are intented to represent higher level
 *      features, additional details maybe negotiated
 *      with key-value pairs specific to the protocol.
 *
 * Enums added to this list should be assigned power-of-two values
 * to facilitate exchanging and comparing bitmaps for supported
 * features.
 *
 * @enum {number}
 */
export declare enum Feature {
    /**
     * Needed to make flatbuffers happy.
     */
    UNUSED = 0,
    /**
     * The stream makes use of multiple full dictionaries with the
     * same ID and assumes clients implement dictionary replacement
     * correctly.
     */
    DICTIONARY_REPLACEMENT = 1,
    /**
     * The stream makes use of compressed bodies as described
     * in Message.fbs.
     */
    COMPRESSED_BODY = 2
}
/**
 * @enum {number}
 */
export declare enum UnionMode {
    Sparse = 0,
    Dense = 1
}
/**
 * @enum {number}
 */
export declare enum Precision {
    HALF = 0,
    SINGLE = 1,
    DOUBLE = 2
}
/**
 * @enum {number}
 */
export declare enum DateUnit {
    DAY = 0,
    MILLISECOND = 1
}
/**
 * @enum {number}
 */
export declare enum TimeUnit {
    SECOND = 0,
    MILLISECOND = 1,
    MICROSECOND = 2,
    NANOSECOND = 3
}
/**
 * @enum {number}
 */
export declare enum IntervalUnit {
    YEAR_MONTH = 0,
    DAY_TIME = 1
}
/**
 * ----------------------------------------------------------------------
 * Top-level Type value, enabling extensible type-specific metadata. We can
 * add new logical types to Type without breaking backwards compatibility
 *
 * @enum {number}
 */
export declare enum Type {
    NONE = 0,
    Null = 1,
    Int = 2,
    FloatingPoint = 3,
    Binary = 4,
    Utf8 = 5,
    Bool = 6,
    Decimal = 7,
    Date = 8,
    Time = 9,
    Timestamp = 10,
    Interval = 11,
    List = 12,
    Struct_ = 13,
    Union = 14,
    FixedSizeBinary = 15,
    FixedSizeList = 16,
    Map = 17,
    Duration = 18,
    LargeBinary = 19,
    LargeUtf8 = 20,
    LargeList = 21
}
/**
 * ----------------------------------------------------------------------
 * Dictionary encoding metadata
 * Maintained for forwards compatibility, in the future
 * Dictionaries might be explicit maps between integers and values
 * allowing for non-contiguous index values
 *
 * @enum {number}
 */
export declare enum DictionaryKind {
    DenseArray = 0
}
/**
 * ----------------------------------------------------------------------
 * Endianness of the platform producing the data
 *
 * @enum {number}
 */
export declare enum Endianness {
    Little = 0,
    Big = 1
}
/**
 * These are stored in the flatbuffer in the Type union below
 *
 * @constructor
 */
export declare class Null {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Null
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Null;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Null= obj
     * @returns Null
     */
    static getRootAsNull(bb: flatbuffers.ByteBuffer, obj?: Null): Null;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Null= obj
     * @returns Null
     */
    static getSizePrefixedRootAsNull(bb: flatbuffers.ByteBuffer, obj?: Null): Null;
    /**
     * @param flatbuffers.Builder builder
     */
    static startNull(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endNull(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createNull(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * A Struct_ in the flatbuffer metadata is the same as an Arrow Struct
 * (according to the physical memory layout). We used Struct_ here as
 * Struct is a reserved word in Flatbuffers
 *
 * @constructor
 */
export declare class Struct_ {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Struct_
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Struct_;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Struct_= obj
     * @returns Struct_
     */
    static getRootAsStruct_(bb: flatbuffers.ByteBuffer, obj?: Struct_): Struct_;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Struct_= obj
     * @returns Struct_
     */
    static getSizePrefixedRootAsStruct_(bb: flatbuffers.ByteBuffer, obj?: Struct_): Struct_;
    /**
     * @param flatbuffers.Builder builder
     */
    static startStruct_(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endStruct_(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createStruct_(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class List {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns List
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): List;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param List= obj
     * @returns List
     */
    static getRootAsList(bb: flatbuffers.ByteBuffer, obj?: List): List;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param List= obj
     * @returns List
     */
    static getSizePrefixedRootAsList(bb: flatbuffers.ByteBuffer, obj?: List): List;
    /**
     * @param flatbuffers.Builder builder
     */
    static startList(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endList(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createList(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * Same as List, but with 64-bit offsets, allowing to represent
 * extremely large data values.
 *
 * @constructor
 */
export declare class LargeList {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns LargeList
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): LargeList;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeList= obj
     * @returns LargeList
     */
    static getRootAsLargeList(bb: flatbuffers.ByteBuffer, obj?: LargeList): LargeList;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeList= obj
     * @returns LargeList
     */
    static getSizePrefixedRootAsLargeList(bb: flatbuffers.ByteBuffer, obj?: LargeList): LargeList;
    /**
     * @param flatbuffers.Builder builder
     */
    static startLargeList(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endLargeList(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createLargeList(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class FixedSizeList {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns FixedSizeList
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): FixedSizeList;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FixedSizeList= obj
     * @returns FixedSizeList
     */
    static getRootAsFixedSizeList(bb: flatbuffers.ByteBuffer, obj?: FixedSizeList): FixedSizeList;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FixedSizeList= obj
     * @returns FixedSizeList
     */
    static getSizePrefixedRootAsFixedSizeList(bb: flatbuffers.ByteBuffer, obj?: FixedSizeList): FixedSizeList;
    /**
     * Number of list items per value
     *
     * @returns number
     */
    listSize(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startFixedSizeList(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number listSize
     */
    static addListSize(builder: flatbuffers.Builder, listSize: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endFixedSizeList(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createFixedSizeList(builder: flatbuffers.Builder, listSize: number): flatbuffers.Offset;
}
/**
 * A Map is a logical nested type that is represented as
 *
 * List<entries: Struct<key: K, value: V>>
 *
 * In this layout, the keys and values are each respectively contiguous. We do
 * not constrain the key and value types, so the application is responsible
 * for ensuring that the keys are hashable and unique. Whether the keys are sorted
 * may be set in the metadata for this field.
 *
 * In a field with Map type, the field has a child Struct field, which then
 * has two children: key type and the second the value type. The names of the
 * child fields may be respectively "entries", "key", and "value", but this is
 * not enforced.
 *
 * Map
 *   - child[0] entries: Struct
 *     - child[0] key: K
 *     - child[1] value: V
 *
 * Neither the "entries" field nor the "key" field may be nullable.
 *
 * The metadata is structured so that Arrow systems without special handling
 * for Map can make Map an alias for List. The "layout" attribute for the Map
 * field must have the same contents as a List.
 *
 * @constructor
 */
export declare class Map {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Map
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Map;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Map= obj
     * @returns Map
     */
    static getRootAsMap(bb: flatbuffers.ByteBuffer, obj?: Map): Map;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Map= obj
     * @returns Map
     */
    static getSizePrefixedRootAsMap(bb: flatbuffers.ByteBuffer, obj?: Map): Map;
    /**
     * Set to true if the keys within each value are sorted
     *
     * @returns boolean
     */
    keysSorted(): boolean;
    /**
     * @param flatbuffers.Builder builder
     */
    static startMap(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param boolean keysSorted
     */
    static addKeysSorted(builder: flatbuffers.Builder, keysSorted: boolean): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endMap(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createMap(builder: flatbuffers.Builder, keysSorted: boolean): flatbuffers.Offset;
}
/**
 * A union is a complex type with children in Field
 * By default ids in the type vector refer to the offsets in the children
 * optionally typeIds provides an indirection between the child offset and the type id
 * for each child typeIds[offset] is the id used in the type vector
 *
 * @constructor
 */
export declare class Union {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Union
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Union;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Union= obj
     * @returns Union
     */
    static getRootAsUnion(bb: flatbuffers.ByteBuffer, obj?: Union): Union;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Union= obj
     * @returns Union
     */
    static getSizePrefixedRootAsUnion(bb: flatbuffers.ByteBuffer, obj?: Union): Union;
    /**
     * @returns UnionMode
     */
    mode(): UnionMode;
    /**
     * @param number index
     * @returns number
     */
    typeIds(index: number): number | null;
    /**
     * @returns number
     */
    typeIdsLength(): number;
    /**
     * @returns Int32Array
     */
    typeIdsArray(): Int32Array | null;
    /**
     * @param flatbuffers.Builder builder
     */
    static startUnion(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param UnionMode mode
     */
    static addMode(builder: flatbuffers.Builder, mode: UnionMode): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset typeIdsOffset
     */
    static addTypeIds(builder: flatbuffers.Builder, typeIdsOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<number> data
     * @returns flatbuffers.Offset
     */
    static createTypeIdsVector(builder: flatbuffers.Builder, data: number[] | Int32Array): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startTypeIdsVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endUnion(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createUnion(builder: flatbuffers.Builder, mode: UnionMode, typeIdsOffset: flatbuffers.Offset): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class Int {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Int
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Int;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Int= obj
     * @returns Int
     */
    static getRootAsInt(bb: flatbuffers.ByteBuffer, obj?: Int): Int;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Int= obj
     * @returns Int
     */
    static getSizePrefixedRootAsInt(bb: flatbuffers.ByteBuffer, obj?: Int): Int;
    /**
     * @returns number
     */
    bitWidth(): number;
    /**
     * @returns boolean
     */
    isSigned(): boolean;
    /**
     * @param flatbuffers.Builder builder
     */
    static startInt(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number bitWidth
     */
    static addBitWidth(builder: flatbuffers.Builder, bitWidth: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param boolean isSigned
     */
    static addIsSigned(builder: flatbuffers.Builder, isSigned: boolean): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endInt(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createInt(builder: flatbuffers.Builder, bitWidth: number, isSigned: boolean): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class FloatingPoint {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns FloatingPoint
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): FloatingPoint;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FloatingPoint= obj
     * @returns FloatingPoint
     */
    static getRootAsFloatingPoint(bb: flatbuffers.ByteBuffer, obj?: FloatingPoint): FloatingPoint;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FloatingPoint= obj
     * @returns FloatingPoint
     */
    static getSizePrefixedRootAsFloatingPoint(bb: flatbuffers.ByteBuffer, obj?: FloatingPoint): FloatingPoint;
    /**
     * @returns Precision
     */
    precision(): Precision;
    /**
     * @param flatbuffers.Builder builder
     */
    static startFloatingPoint(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Precision precision
     */
    static addPrecision(builder: flatbuffers.Builder, precision: Precision): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endFloatingPoint(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createFloatingPoint(builder: flatbuffers.Builder, precision: Precision): flatbuffers.Offset;
}
/**
 * Unicode with UTF-8 encoding
 *
 * @constructor
 */
export declare class Utf8 {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Utf8
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Utf8;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Utf8= obj
     * @returns Utf8
     */
    static getRootAsUtf8(bb: flatbuffers.ByteBuffer, obj?: Utf8): Utf8;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Utf8= obj
     * @returns Utf8
     */
    static getSizePrefixedRootAsUtf8(bb: flatbuffers.ByteBuffer, obj?: Utf8): Utf8;
    /**
     * @param flatbuffers.Builder builder
     */
    static startUtf8(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endUtf8(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createUtf8(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * Opaque binary data
 *
 * @constructor
 */
export declare class Binary {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Binary
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Binary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Binary= obj
     * @returns Binary
     */
    static getRootAsBinary(bb: flatbuffers.ByteBuffer, obj?: Binary): Binary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Binary= obj
     * @returns Binary
     */
    static getSizePrefixedRootAsBinary(bb: flatbuffers.ByteBuffer, obj?: Binary): Binary;
    /**
     * @param flatbuffers.Builder builder
     */
    static startBinary(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endBinary(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createBinary(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * Same as Utf8, but with 64-bit offsets, allowing to represent
 * extremely large data values.
 *
 * @constructor
 */
export declare class LargeUtf8 {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns LargeUtf8
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): LargeUtf8;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeUtf8= obj
     * @returns LargeUtf8
     */
    static getRootAsLargeUtf8(bb: flatbuffers.ByteBuffer, obj?: LargeUtf8): LargeUtf8;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeUtf8= obj
     * @returns LargeUtf8
     */
    static getSizePrefixedRootAsLargeUtf8(bb: flatbuffers.ByteBuffer, obj?: LargeUtf8): LargeUtf8;
    /**
     * @param flatbuffers.Builder builder
     */
    static startLargeUtf8(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endLargeUtf8(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createLargeUtf8(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * Same as Binary, but with 64-bit offsets, allowing to represent
 * extremely large data values.
 *
 * @constructor
 */
export declare class LargeBinary {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns LargeBinary
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): LargeBinary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeBinary= obj
     * @returns LargeBinary
     */
    static getRootAsLargeBinary(bb: flatbuffers.ByteBuffer, obj?: LargeBinary): LargeBinary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param LargeBinary= obj
     * @returns LargeBinary
     */
    static getSizePrefixedRootAsLargeBinary(bb: flatbuffers.ByteBuffer, obj?: LargeBinary): LargeBinary;
    /**
     * @param flatbuffers.Builder builder
     */
    static startLargeBinary(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endLargeBinary(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createLargeBinary(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class FixedSizeBinary {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns FixedSizeBinary
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): FixedSizeBinary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FixedSizeBinary= obj
     * @returns FixedSizeBinary
     */
    static getRootAsFixedSizeBinary(bb: flatbuffers.ByteBuffer, obj?: FixedSizeBinary): FixedSizeBinary;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param FixedSizeBinary= obj
     * @returns FixedSizeBinary
     */
    static getSizePrefixedRootAsFixedSizeBinary(bb: flatbuffers.ByteBuffer, obj?: FixedSizeBinary): FixedSizeBinary;
    /**
     * Number of bytes per value
     *
     * @returns number
     */
    byteWidth(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startFixedSizeBinary(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number byteWidth
     */
    static addByteWidth(builder: flatbuffers.Builder, byteWidth: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endFixedSizeBinary(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createFixedSizeBinary(builder: flatbuffers.Builder, byteWidth: number): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class Bool {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Bool
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Bool;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Bool= obj
     * @returns Bool
     */
    static getRootAsBool(bb: flatbuffers.ByteBuffer, obj?: Bool): Bool;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Bool= obj
     * @returns Bool
     */
    static getSizePrefixedRootAsBool(bb: flatbuffers.ByteBuffer, obj?: Bool): Bool;
    /**
     * @param flatbuffers.Builder builder
     */
    static startBool(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endBool(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createBool(builder: flatbuffers.Builder): flatbuffers.Offset;
}
/**
 * Exact decimal value represented as an integer value in two's
 * complement. Currently only 128-bit (16-byte) and 256-bit (32-byte) integers
 * are used. The representation uses the endianness indicated
 * in the Schema.
 *
 * @constructor
 */
export declare class Decimal {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Decimal
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Decimal;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Decimal= obj
     * @returns Decimal
     */
    static getRootAsDecimal(bb: flatbuffers.ByteBuffer, obj?: Decimal): Decimal;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Decimal= obj
     * @returns Decimal
     */
    static getSizePrefixedRootAsDecimal(bb: flatbuffers.ByteBuffer, obj?: Decimal): Decimal;
    /**
     * Total number of decimal digits
     *
     * @returns number
     */
    precision(): number;
    /**
     * Number of digits after the decimal point "."
     *
     * @returns number
     */
    scale(): number;
    /**
     * Number of bits per value. The only accepted widths are 128 and 256.
     * We use bitWidth for consistency with Int::bitWidth.
     *
     * @returns number
     */
    bitWidth(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startDecimal(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number precision
     */
    static addPrecision(builder: flatbuffers.Builder, precision: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number scale
     */
    static addScale(builder: flatbuffers.Builder, scale: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number bitWidth
     */
    static addBitWidth(builder: flatbuffers.Builder, bitWidth: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endDecimal(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createDecimal(builder: flatbuffers.Builder, precision: number, scale: number, bitWidth: number): flatbuffers.Offset;
}
/**
 * Date is either a 32-bit or 64-bit type representing elapsed time since UNIX
 * epoch (1970-01-01), stored in either of two units:
 *
 * * Milliseconds (64 bits) indicating UNIX time elapsed since the epoch (no
 *   leap seconds), where the values are evenly divisible by 86400000
 * * Days (32 bits) since the UNIX epoch
 *
 * @constructor
 */
export declare class Date {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Date
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Date;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Date= obj
     * @returns Date
     */
    static getRootAsDate(bb: flatbuffers.ByteBuffer, obj?: Date): Date;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Date= obj
     * @returns Date
     */
    static getSizePrefixedRootAsDate(bb: flatbuffers.ByteBuffer, obj?: Date): Date;
    /**
     * @returns DateUnit
     */
    unit(): DateUnit;
    /**
     * @param flatbuffers.Builder builder
     */
    static startDate(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param DateUnit unit
     */
    static addUnit(builder: flatbuffers.Builder, unit: DateUnit): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endDate(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createDate(builder: flatbuffers.Builder, unit: DateUnit): flatbuffers.Offset;
}
/**
 * Time type. The physical storage type depends on the unit
 * - SECOND and MILLISECOND: 32 bits
 * - MICROSECOND and NANOSECOND: 64 bits
 *
 * @constructor
 */
export declare class Time {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Time
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Time;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Time= obj
     * @returns Time
     */
    static getRootAsTime(bb: flatbuffers.ByteBuffer, obj?: Time): Time;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Time= obj
     * @returns Time
     */
    static getSizePrefixedRootAsTime(bb: flatbuffers.ByteBuffer, obj?: Time): Time;
    /**
     * @returns TimeUnit
     */
    unit(): TimeUnit;
    /**
     * @returns number
     */
    bitWidth(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startTime(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param TimeUnit unit
     */
    static addUnit(builder: flatbuffers.Builder, unit: TimeUnit): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number bitWidth
     */
    static addBitWidth(builder: flatbuffers.Builder, bitWidth: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endTime(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createTime(builder: flatbuffers.Builder, unit: TimeUnit, bitWidth: number): flatbuffers.Offset;
}
/**
 * Time elapsed from the Unix epoch, 00:00:00.000 on 1 January 1970, excluding
 * leap seconds, as a 64-bit integer. Note that UNIX time does not include
 * leap seconds.
 *
 * The Timestamp metadata supports both "time zone naive" and "time zone
 * aware" timestamps. Read about the timezone attribute for more detail
 *
 * @constructor
 */
export declare class Timestamp {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Timestamp
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Timestamp;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Timestamp= obj
     * @returns Timestamp
     */
    static getRootAsTimestamp(bb: flatbuffers.ByteBuffer, obj?: Timestamp): Timestamp;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Timestamp= obj
     * @returns Timestamp
     */
    static getSizePrefixedRootAsTimestamp(bb: flatbuffers.ByteBuffer, obj?: Timestamp): Timestamp;
    /**
     * @returns TimeUnit
     */
    unit(): TimeUnit;
    /**
     * The time zone is a string indicating the name of a time zone, one of:
     *
     * * As used in the Olson time zone database (the "tz database" or
     *   "tzdata"), such as "America/New_York"
     * * An absolute time zone offset of the form +XX:XX or -XX:XX, such as +07:30
     *
     * Whether a timezone string is present indicates different semantics about
     * the data:
     *
     * * If the time zone is null or equal to an empty string, the data is "time
     *   zone naive" and shall be displayed *as is* to the user, not localized
     *   to the locale of the user. This data can be though of as UTC but
     *   without having "UTC" as the time zone, it is not considered to be
     *   localized to any time zone
     *
     * * If the time zone is set to a valid value, values can be displayed as
     *   "localized" to that time zone, even though the underlying 64-bit
     *   integers are identical to the same data stored in UTC. Converting
     *   between time zones is a metadata-only operation and does not change the
     *   underlying values
     *
     * @param flatbuffers.Encoding= optionalEncoding
     * @returns string|Uint8Array|null
     */
    timezone(): string | null;
    timezone(optionalEncoding: flatbuffers.Encoding): string | Uint8Array | null;
    /**
     * @param flatbuffers.Builder builder
     */
    static startTimestamp(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param TimeUnit unit
     */
    static addUnit(builder: flatbuffers.Builder, unit: TimeUnit): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset timezoneOffset
     */
    static addTimezone(builder: flatbuffers.Builder, timezoneOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endTimestamp(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createTimestamp(builder: flatbuffers.Builder, unit: TimeUnit, timezoneOffset: flatbuffers.Offset): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class Interval {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Interval
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Interval;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Interval= obj
     * @returns Interval
     */
    static getRootAsInterval(bb: flatbuffers.ByteBuffer, obj?: Interval): Interval;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Interval= obj
     * @returns Interval
     */
    static getSizePrefixedRootAsInterval(bb: flatbuffers.ByteBuffer, obj?: Interval): Interval;
    /**
     * @returns IntervalUnit
     */
    unit(): IntervalUnit;
    /**
     * @param flatbuffers.Builder builder
     */
    static startInterval(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param IntervalUnit unit
     */
    static addUnit(builder: flatbuffers.Builder, unit: IntervalUnit): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endInterval(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createInterval(builder: flatbuffers.Builder, unit: IntervalUnit): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class Duration {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Duration
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Duration;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Duration= obj
     * @returns Duration
     */
    static getRootAsDuration(bb: flatbuffers.ByteBuffer, obj?: Duration): Duration;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Duration= obj
     * @returns Duration
     */
    static getSizePrefixedRootAsDuration(bb: flatbuffers.ByteBuffer, obj?: Duration): Duration;
    /**
     * @returns TimeUnit
     */
    unit(): TimeUnit;
    /**
     * @param flatbuffers.Builder builder
     */
    static startDuration(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param TimeUnit unit
     */
    static addUnit(builder: flatbuffers.Builder, unit: TimeUnit): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endDuration(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createDuration(builder: flatbuffers.Builder, unit: TimeUnit): flatbuffers.Offset;
}
/**
 * ----------------------------------------------------------------------
 * user defined key value pairs to add custom metadata to arrow
 * key namespacing is the responsibility of the user
 *
 * @constructor
 */
export declare class KeyValue {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns KeyValue
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): KeyValue;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param KeyValue= obj
     * @returns KeyValue
     */
    static getRootAsKeyValue(bb: flatbuffers.ByteBuffer, obj?: KeyValue): KeyValue;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param KeyValue= obj
     * @returns KeyValue
     */
    static getSizePrefixedRootAsKeyValue(bb: flatbuffers.ByteBuffer, obj?: KeyValue): KeyValue;
    /**
     * @param flatbuffers.Encoding= optionalEncoding
     * @returns string|Uint8Array|null
     */
    key(): string | null;
    key(optionalEncoding: flatbuffers.Encoding): string | Uint8Array | null;
    /**
     * @param flatbuffers.Encoding= optionalEncoding
     * @returns string|Uint8Array|null
     */
    value(): string | null;
    value(optionalEncoding: flatbuffers.Encoding): string | Uint8Array | null;
    /**
     * @param flatbuffers.Builder builder
     */
    static startKeyValue(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset keyOffset
     */
    static addKey(builder: flatbuffers.Builder, keyOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset valueOffset
     */
    static addValue(builder: flatbuffers.Builder, valueOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endKeyValue(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createKeyValue(builder: flatbuffers.Builder, keyOffset: flatbuffers.Offset, valueOffset: flatbuffers.Offset): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class DictionaryEncoding {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns DictionaryEncoding
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): DictionaryEncoding;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param DictionaryEncoding= obj
     * @returns DictionaryEncoding
     */
    static getRootAsDictionaryEncoding(bb: flatbuffers.ByteBuffer, obj?: DictionaryEncoding): DictionaryEncoding;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param DictionaryEncoding= obj
     * @returns DictionaryEncoding
     */
    static getSizePrefixedRootAsDictionaryEncoding(bb: flatbuffers.ByteBuffer, obj?: DictionaryEncoding): DictionaryEncoding;
    /**
     * The known dictionary id in the application where this data is used. In
     * the file or streaming formats, the dictionary ids are found in the
     * DictionaryBatch messages
     *
     * @returns flatbuffers.Long
     */
    id(): flatbuffers.Long;
    /**
     * The dictionary indices are constrained to be non-negative integers. If
     * this field is null, the indices must be signed int32. To maximize
     * cross-language compatibility and performance, implementations are
     * recommended to prefer signed integer types over unsigned integer types
     * and to avoid uint64 indices unless they are required by an application.
     *
     * @param Int= obj
     * @returns Int|null
     */
    indexType(obj?: Int): Int | null;
    /**
     * By default, dictionaries are not ordered, or the order does not have
     * semantic meaning. In some statistical, applications, dictionary-encoding
     * is used to represent ordered categorical data, and we provide a way to
     * preserve that metadata here
     *
     * @returns boolean
     */
    isOrdered(): boolean;
    /**
     * @returns DictionaryKind
     */
    dictionaryKind(): DictionaryKind;
    /**
     * @param flatbuffers.Builder builder
     */
    static startDictionaryEncoding(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Long id
     */
    static addId(builder: flatbuffers.Builder, id: flatbuffers.Long): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset indexTypeOffset
     */
    static addIndexType(builder: flatbuffers.Builder, indexTypeOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param boolean isOrdered
     */
    static addIsOrdered(builder: flatbuffers.Builder, isOrdered: boolean): void;
    /**
     * @param flatbuffers.Builder builder
     * @param DictionaryKind dictionaryKind
     */
    static addDictionaryKind(builder: flatbuffers.Builder, dictionaryKind: DictionaryKind): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endDictionaryEncoding(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createDictionaryEncoding(builder: flatbuffers.Builder, id: flatbuffers.Long, indexTypeOffset: flatbuffers.Offset, isOrdered: boolean, dictionaryKind: DictionaryKind): flatbuffers.Offset;
}
/**
 * ----------------------------------------------------------------------
 * A field represents a named column in a record / row batch or child of a
 * nested type.
 *
 * @constructor
 */
export declare class Field {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Field
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Field;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Field= obj
     * @returns Field
     */
    static getRootAsField(bb: flatbuffers.ByteBuffer, obj?: Field): Field;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Field= obj
     * @returns Field
     */
    static getSizePrefixedRootAsField(bb: flatbuffers.ByteBuffer, obj?: Field): Field;
    /**
     * Name is not required, in i.e. a List
     *
     * @param flatbuffers.Encoding= optionalEncoding
     * @returns string|Uint8Array|null
     */
    name(): string | null;
    name(optionalEncoding: flatbuffers.Encoding): string | Uint8Array | null;
    /**
     * Whether or not this field can contain nulls. Should be true in general.
     *
     * @returns boolean
     */
    nullable(): boolean;
    /**
     * @returns Type
     */
    typeType(): Type;
    /**
     * This is the type of the decoded value if the field is dictionary encoded.
     *
     * @param flatbuffers.Table obj
     * @returns ?flatbuffers.Table
     */
    type<T extends flatbuffers.Table>(obj: T): T | null;
    /**
     * Present only if the field is dictionary encoded.
     *
     * @param DictionaryEncoding= obj
     * @returns DictionaryEncoding|null
     */
    dictionary(obj?: DictionaryEncoding): DictionaryEncoding | null;
    /**
     * children apply only to nested data types like Struct, List and Union. For
     * primitive types children will have length 0.
     *
     * @param number index
     * @param Field= obj
     * @returns Field
     */
    children(index: number, obj?: Field): Field | null;
    /**
     * @returns number
     */
    childrenLength(): number;
    /**
     * User-defined metadata
     *
     * @param number index
     * @param KeyValue= obj
     * @returns KeyValue
     */
    customMetadata(index: number, obj?: KeyValue): KeyValue | null;
    /**
     * @returns number
     */
    customMetadataLength(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startField(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset nameOffset
     */
    static addName(builder: flatbuffers.Builder, nameOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param boolean nullable
     */
    static addNullable(builder: flatbuffers.Builder, nullable: boolean): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Type typeType
     */
    static addTypeType(builder: flatbuffers.Builder, typeType: Type): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset typeOffset
     */
    static addType(builder: flatbuffers.Builder, typeOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset dictionaryOffset
     */
    static addDictionary(builder: flatbuffers.Builder, dictionaryOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset childrenOffset
     */
    static addChildren(builder: flatbuffers.Builder, childrenOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<flatbuffers.Offset> data
     * @returns flatbuffers.Offset
     */
    static createChildrenVector(builder: flatbuffers.Builder, data: flatbuffers.Offset[]): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startChildrenVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset customMetadataOffset
     */
    static addCustomMetadata(builder: flatbuffers.Builder, customMetadataOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<flatbuffers.Offset> data
     * @returns flatbuffers.Offset
     */
    static createCustomMetadataVector(builder: flatbuffers.Builder, data: flatbuffers.Offset[]): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startCustomMetadataVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endField(builder: flatbuffers.Builder): flatbuffers.Offset;
    static createField(builder: flatbuffers.Builder, nameOffset: flatbuffers.Offset, nullable: boolean, typeType: Type, typeOffset: flatbuffers.Offset, dictionaryOffset: flatbuffers.Offset, childrenOffset: flatbuffers.Offset, customMetadataOffset: flatbuffers.Offset): flatbuffers.Offset;
}
/**
 * ----------------------------------------------------------------------
 * A Buffer represents a single contiguous memory segment
 *
 * @constructor
 */
export declare class Buffer {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Buffer
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Buffer;
    /**
     * The relative offset into the shared memory page where the bytes for this
     * buffer starts
     *
     * @returns flatbuffers.Long
     */
    offset(): flatbuffers.Long;
    /**
     * The absolute length (in bytes) of the memory buffer. The memory is found
     * from offset (inclusive) to offset + length (non-inclusive). When building
     * messages using the encapsulated IPC message, padding bytes may be written
     * after a buffer, but such padding bytes do not need to be accounted for in
     * the size here.
     *
     * @returns flatbuffers.Long
     */
    length(): flatbuffers.Long;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Long offset
     * @param flatbuffers.Long length
     * @returns flatbuffers.Offset
     */
    static createBuffer(builder: flatbuffers.Builder, offset: flatbuffers.Long, length: flatbuffers.Long): flatbuffers.Offset;
}
/**
 * ----------------------------------------------------------------------
 * A Schema describes the columns in a row batch
 *
 * @constructor
 */
export declare class Schema {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Schema
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Schema;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Schema= obj
     * @returns Schema
     */
    static getRootAsSchema(bb: flatbuffers.ByteBuffer, obj?: Schema): Schema;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Schema= obj
     * @returns Schema
     */
    static getSizePrefixedRootAsSchema(bb: flatbuffers.ByteBuffer, obj?: Schema): Schema;
    /**
     * endianness of the buffer
     * it is Little Endian by default
     * if endianness doesn't match the underlying system then the vectors need to be converted
     *
     * @returns Endianness
     */
    endianness(): Endianness;
    /**
     * @param number index
     * @param Field= obj
     * @returns Field
     */
    fields(index: number, obj?: Field): Field | null;
    /**
     * @returns number
     */
    fieldsLength(): number;
    /**
     * @param number index
     * @param KeyValue= obj
     * @returns KeyValue
     */
    customMetadata(index: number, obj?: KeyValue): KeyValue | null;
    /**
     * @returns number
     */
    customMetadataLength(): number;
    /**
     * Features used in the stream/file.
     *
     * @param number index
     * @returns flatbuffers.Long
     */
    features(index: number): flatbuffers.Long | null;
    /**
     * @returns number
     */
    featuresLength(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startSchema(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Endianness endianness
     */
    static addEndianness(builder: flatbuffers.Builder, endianness: Endianness): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset fieldsOffset
     */
    static addFields(builder: flatbuffers.Builder, fieldsOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<flatbuffers.Offset> data
     * @returns flatbuffers.Offset
     */
    static createFieldsVector(builder: flatbuffers.Builder, data: flatbuffers.Offset[]): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startFieldsVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset customMetadataOffset
     */
    static addCustomMetadata(builder: flatbuffers.Builder, customMetadataOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<flatbuffers.Offset> data
     * @returns flatbuffers.Offset
     */
    static createCustomMetadataVector(builder: flatbuffers.Builder, data: flatbuffers.Offset[]): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startCustomMetadataVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset featuresOffset
     */
    static addFeatures(builder: flatbuffers.Builder, featuresOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param Array.<flatbuffers.Long> data
     * @returns flatbuffers.Offset
     */
    static createFeaturesVector(builder: flatbuffers.Builder, data: flatbuffers.Long[]): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startFeaturesVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @returns flatbuffers.Offset
     */
    static endSchema(builder: flatbuffers.Builder): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset offset
     */
    static finishSchemaBuffer(builder: flatbuffers.Builder, offset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset offset
     */
    static finishSizePrefixedSchemaBuffer(builder: flatbuffers.Builder, offset: flatbuffers.Offset): void;
    static createSchema(builder: flatbuffers.Builder, endianness: Endianness, fieldsOffset: flatbuffers.Offset, customMetadataOffset: flatbuffers.Offset, featuresOffset: flatbuffers.Offset): flatbuffers.Offset;
}
