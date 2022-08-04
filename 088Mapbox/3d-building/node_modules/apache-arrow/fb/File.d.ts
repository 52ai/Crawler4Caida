import { flatbuffers } from 'flatbuffers';
import * as NS13596923344997147894 from './Schema';
/**
 * ----------------------------------------------------------------------
 * Arrow File metadata
 *
 *
 * @constructor
 */
export declare class Footer {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Footer
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Footer;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Footer= obj
     * @returns Footer
     */
    static getRootAsFooter(bb: flatbuffers.ByteBuffer, obj?: Footer): Footer;
    /**
     * @param flatbuffers.ByteBuffer bb
     * @param Footer= obj
     * @returns Footer
     */
    static getSizePrefixedRootAsFooter(bb: flatbuffers.ByteBuffer, obj?: Footer): Footer;
    /**
     * @returns MetadataVersion
     */
    version(): NS13596923344997147894.MetadataVersion;
    /**
     * @param Schema= obj
     * @returns Schema|null
     */
    schema(obj?: NS13596923344997147894.Schema): NS13596923344997147894.Schema | null;
    /**
     * @param number index
     * @param Block= obj
     * @returns Block
     */
    dictionaries(index: number, obj?: Block): Block | null;
    /**
     * @returns number
     */
    dictionariesLength(): number;
    /**
     * @param number index
     * @param Block= obj
     * @returns Block
     */
    recordBatches(index: number, obj?: Block): Block | null;
    /**
     * @returns number
     */
    recordBatchesLength(): number;
    /**
     * User-defined metadata
     *
     * @param number index
     * @param KeyValue= obj
     * @returns KeyValue
     */
    customMetadata(index: number, obj?: NS13596923344997147894.KeyValue): NS13596923344997147894.KeyValue | null;
    /**
     * @returns number
     */
    customMetadataLength(): number;
    /**
     * @param flatbuffers.Builder builder
     */
    static startFooter(builder: flatbuffers.Builder): void;
    /**
     * @param flatbuffers.Builder builder
     * @param MetadataVersion version
     */
    static addVersion(builder: flatbuffers.Builder, version: NS13596923344997147894.MetadataVersion): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset schemaOffset
     */
    static addSchema(builder: flatbuffers.Builder, schemaOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset dictionariesOffset
     */
    static addDictionaries(builder: flatbuffers.Builder, dictionariesOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startDictionariesVector(builder: flatbuffers.Builder, numElems: number): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset recordBatchesOffset
     */
    static addRecordBatches(builder: flatbuffers.Builder, recordBatchesOffset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param number numElems
     */
    static startRecordBatchesVector(builder: flatbuffers.Builder, numElems: number): void;
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
    static endFooter(builder: flatbuffers.Builder): flatbuffers.Offset;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset offset
     */
    static finishFooterBuffer(builder: flatbuffers.Builder, offset: flatbuffers.Offset): void;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Offset offset
     */
    static finishSizePrefixedFooterBuffer(builder: flatbuffers.Builder, offset: flatbuffers.Offset): void;
    static createFooter(builder: flatbuffers.Builder, version: NS13596923344997147894.MetadataVersion, schemaOffset: flatbuffers.Offset, dictionariesOffset: flatbuffers.Offset, recordBatchesOffset: flatbuffers.Offset, customMetadataOffset: flatbuffers.Offset): flatbuffers.Offset;
}
/**
 * @constructor
 */
export declare class Block {
    bb: flatbuffers.ByteBuffer | null;
    bb_pos: number;
    /**
     * @param number i
     * @param flatbuffers.ByteBuffer bb
     * @returns Block
     */
    __init(i: number, bb: flatbuffers.ByteBuffer): Block;
    /**
     * Index to the start of the RecordBlock (note this is past the Message header)
     *
     * @returns flatbuffers.Long
     */
    offset(): flatbuffers.Long;
    /**
     * Length of the metadata
     *
     * @returns number
     */
    metaDataLength(): number;
    /**
     * Length of the data (this is aligned so there can be a gap between this and
     * the metadata).
     *
     * @returns flatbuffers.Long
     */
    bodyLength(): flatbuffers.Long;
    /**
     * @param flatbuffers.Builder builder
     * @param flatbuffers.Long offset
     * @param number metaDataLength
     * @param flatbuffers.Long bodyLength
     * @returns flatbuffers.Offset
     */
    static createBlock(builder: flatbuffers.Builder, offset: flatbuffers.Long, metaDataLength: number, bodyLength: flatbuffers.Long): flatbuffers.Offset;
}
