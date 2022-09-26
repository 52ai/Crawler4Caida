"use strict";
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
Object.defineProperty(exports, "__esModule", { value: true });
exports.vectorFromValuesWithType = exports.StructRow = exports.MapRow = exports.Utf8Vector = exports.SparseUnionVector = exports.DenseUnionVector = exports.UnionVector = exports.TimeNanosecondVector = exports.TimeMicrosecondVector = exports.TimeMillisecondVector = exports.TimeSecondVector = exports.TimeVector = exports.TimestampNanosecondVector = exports.TimestampMicrosecondVector = exports.TimestampMillisecondVector = exports.TimestampSecondVector = exports.TimestampVector = exports.StructVector = exports.NullVector = exports.MapVector = exports.ListVector = exports.Uint64Vector = exports.Uint32Vector = exports.Uint16Vector = exports.Uint8Vector = exports.Int64Vector = exports.Int32Vector = exports.Int16Vector = exports.Int8Vector = exports.IntVector = exports.IntervalYearMonthVector = exports.IntervalDayTimeVector = exports.IntervalVector = exports.Float64Vector = exports.Float32Vector = exports.Float16Vector = exports.FloatVector = exports.FixedSizeListVector = exports.FixedSizeBinaryVector = exports.DictionaryVector = exports.DecimalVector = exports.DateMillisecondVector = exports.DateDayVector = exports.DateVector = exports.Chunked = exports.BoolVector = exports.BinaryVector = exports.BaseVector = exports.Vector = void 0;
var vector_1 = require("../vector");
Object.defineProperty(exports, "Vector", { enumerable: true, get: function () { return vector_1.Vector; } });
var base_1 = require("./base");
Object.defineProperty(exports, "BaseVector", { enumerable: true, get: function () { return base_1.BaseVector; } });
var binary_1 = require("./binary");
Object.defineProperty(exports, "BinaryVector", { enumerable: true, get: function () { return binary_1.BinaryVector; } });
var bool_1 = require("./bool");
Object.defineProperty(exports, "BoolVector", { enumerable: true, get: function () { return bool_1.BoolVector; } });
var chunked_1 = require("./chunked");
Object.defineProperty(exports, "Chunked", { enumerable: true, get: function () { return chunked_1.Chunked; } });
var date_1 = require("./date");
Object.defineProperty(exports, "DateVector", { enumerable: true, get: function () { return date_1.DateVector; } });
Object.defineProperty(exports, "DateDayVector", { enumerable: true, get: function () { return date_1.DateDayVector; } });
Object.defineProperty(exports, "DateMillisecondVector", { enumerable: true, get: function () { return date_1.DateMillisecondVector; } });
var decimal_1 = require("./decimal");
Object.defineProperty(exports, "DecimalVector", { enumerable: true, get: function () { return decimal_1.DecimalVector; } });
var dictionary_1 = require("./dictionary");
Object.defineProperty(exports, "DictionaryVector", { enumerable: true, get: function () { return dictionary_1.DictionaryVector; } });
var fixedsizebinary_1 = require("./fixedsizebinary");
Object.defineProperty(exports, "FixedSizeBinaryVector", { enumerable: true, get: function () { return fixedsizebinary_1.FixedSizeBinaryVector; } });
var fixedsizelist_1 = require("./fixedsizelist");
Object.defineProperty(exports, "FixedSizeListVector", { enumerable: true, get: function () { return fixedsizelist_1.FixedSizeListVector; } });
var float_1 = require("./float");
Object.defineProperty(exports, "FloatVector", { enumerable: true, get: function () { return float_1.FloatVector; } });
Object.defineProperty(exports, "Float16Vector", { enumerable: true, get: function () { return float_1.Float16Vector; } });
Object.defineProperty(exports, "Float32Vector", { enumerable: true, get: function () { return float_1.Float32Vector; } });
Object.defineProperty(exports, "Float64Vector", { enumerable: true, get: function () { return float_1.Float64Vector; } });
var interval_1 = require("./interval");
Object.defineProperty(exports, "IntervalVector", { enumerable: true, get: function () { return interval_1.IntervalVector; } });
Object.defineProperty(exports, "IntervalDayTimeVector", { enumerable: true, get: function () { return interval_1.IntervalDayTimeVector; } });
Object.defineProperty(exports, "IntervalYearMonthVector", { enumerable: true, get: function () { return interval_1.IntervalYearMonthVector; } });
var int_1 = require("./int");
Object.defineProperty(exports, "IntVector", { enumerable: true, get: function () { return int_1.IntVector; } });
Object.defineProperty(exports, "Int8Vector", { enumerable: true, get: function () { return int_1.Int8Vector; } });
Object.defineProperty(exports, "Int16Vector", { enumerable: true, get: function () { return int_1.Int16Vector; } });
Object.defineProperty(exports, "Int32Vector", { enumerable: true, get: function () { return int_1.Int32Vector; } });
Object.defineProperty(exports, "Int64Vector", { enumerable: true, get: function () { return int_1.Int64Vector; } });
Object.defineProperty(exports, "Uint8Vector", { enumerable: true, get: function () { return int_1.Uint8Vector; } });
Object.defineProperty(exports, "Uint16Vector", { enumerable: true, get: function () { return int_1.Uint16Vector; } });
Object.defineProperty(exports, "Uint32Vector", { enumerable: true, get: function () { return int_1.Uint32Vector; } });
Object.defineProperty(exports, "Uint64Vector", { enumerable: true, get: function () { return int_1.Uint64Vector; } });
var list_1 = require("./list");
Object.defineProperty(exports, "ListVector", { enumerable: true, get: function () { return list_1.ListVector; } });
var map_1 = require("./map");
Object.defineProperty(exports, "MapVector", { enumerable: true, get: function () { return map_1.MapVector; } });
var null_1 = require("./null");
Object.defineProperty(exports, "NullVector", { enumerable: true, get: function () { return null_1.NullVector; } });
var struct_1 = require("./struct");
Object.defineProperty(exports, "StructVector", { enumerable: true, get: function () { return struct_1.StructVector; } });
var timestamp_1 = require("./timestamp");
Object.defineProperty(exports, "TimestampVector", { enumerable: true, get: function () { return timestamp_1.TimestampVector; } });
Object.defineProperty(exports, "TimestampSecondVector", { enumerable: true, get: function () { return timestamp_1.TimestampSecondVector; } });
Object.defineProperty(exports, "TimestampMillisecondVector", { enumerable: true, get: function () { return timestamp_1.TimestampMillisecondVector; } });
Object.defineProperty(exports, "TimestampMicrosecondVector", { enumerable: true, get: function () { return timestamp_1.TimestampMicrosecondVector; } });
Object.defineProperty(exports, "TimestampNanosecondVector", { enumerable: true, get: function () { return timestamp_1.TimestampNanosecondVector; } });
var time_1 = require("./time");
Object.defineProperty(exports, "TimeVector", { enumerable: true, get: function () { return time_1.TimeVector; } });
Object.defineProperty(exports, "TimeSecondVector", { enumerable: true, get: function () { return time_1.TimeSecondVector; } });
Object.defineProperty(exports, "TimeMillisecondVector", { enumerable: true, get: function () { return time_1.TimeMillisecondVector; } });
Object.defineProperty(exports, "TimeMicrosecondVector", { enumerable: true, get: function () { return time_1.TimeMicrosecondVector; } });
Object.defineProperty(exports, "TimeNanosecondVector", { enumerable: true, get: function () { return time_1.TimeNanosecondVector; } });
var union_1 = require("./union");
Object.defineProperty(exports, "UnionVector", { enumerable: true, get: function () { return union_1.UnionVector; } });
Object.defineProperty(exports, "DenseUnionVector", { enumerable: true, get: function () { return union_1.DenseUnionVector; } });
Object.defineProperty(exports, "SparseUnionVector", { enumerable: true, get: function () { return union_1.SparseUnionVector; } });
var utf8_1 = require("./utf8");
Object.defineProperty(exports, "Utf8Vector", { enumerable: true, get: function () { return utf8_1.Utf8Vector; } });
var row_1 = require("./row");
Object.defineProperty(exports, "MapRow", { enumerable: true, get: function () { return row_1.MapRow; } });
Object.defineProperty(exports, "StructRow", { enumerable: true, get: function () { return row_1.StructRow; } });
const fn = require("../util/fn");
const enum_1 = require("../enum");
const vector_2 = require("../vector");
const chunked_2 = require("./chunked");
const base_2 = require("./base");
const bit_1 = require("../util/bit");
const compat_1 = require("../util/compat");
const builder_1 = require("../builder");
const get_1 = require("../visitor/get");
const set_1 = require("../visitor/set");
const indexof_1 = require("../visitor/indexof");
const toarray_1 = require("../visitor/toarray");
const iterator_1 = require("../visitor/iterator");
const bytewidth_1 = require("../visitor/bytewidth");
const vectorctor_1 = require("../visitor/vectorctor");
/** @nocollapse */
vector_2.Vector.new = newVector;
/** @nocollapse */
vector_2.Vector.from = vectorFrom;
/** @ignore */
function newVector(data, ...args) {
    return new (vectorctor_1.instance.getVisitFn(data)())(data, ...args);
}
/** @ignore */
function vectorFromValuesWithType(newDataType, input) {
    if (compat_1.isIterable(input)) {
        return vector_2.Vector.from({ 'nullValues': [null, undefined], type: newDataType(), 'values': input });
    }
    else if (compat_1.isAsyncIterable(input)) {
        return vector_2.Vector.from({ 'nullValues': [null, undefined], type: newDataType(), 'values': input });
    }
    const { 'values': values = [], 'type': type = newDataType(), 'nullValues': nullValues = [null, undefined], } = { ...input };
    return compat_1.isIterable(values)
        ? vector_2.Vector.from({ nullValues, ...input, type })
        : vector_2.Vector.from({ nullValues, ...input, type });
}
exports.vectorFromValuesWithType = vectorFromValuesWithType;
function vectorFrom(input) {
    const { 'values': values = [], ...options } = { 'nullValues': [null, undefined], ...input };
    if (compat_1.isIterable(values)) {
        const chunks = [...builder_1.Builder.throughIterable(options)(values)];
        return (chunks.length === 1 ? chunks[0] : chunked_2.Chunked.concat(chunks));
    }
    return (async (chunks) => {
        const transform = builder_1.Builder.throughAsyncIterable(options);
        for await (const chunk of transform(values)) {
            chunks.push(chunk);
        }
        return (chunks.length === 1 ? chunks[0] : chunked_2.Chunked.concat(chunks));
    })([]);
}
//
// We provide the following method implementations for code navigability purposes only.
// They're overridden at runtime below with the specific Visitor implementation for each type,
// short-circuiting the usual Visitor traversal and reducing intermediate lookups and calls.
// This comment is here to remind you to not set breakpoints in these function bodies, or to inform
// you why the breakpoints you have already set are not being triggered. Have a great day!
//
base_2.BaseVector.prototype.get = function baseVectorGet(index) {
    return get_1.instance.visit(this, index);
};
base_2.BaseVector.prototype.set = function baseVectorSet(index, value) {
    return set_1.instance.visit(this, index, value);
};
base_2.BaseVector.prototype.indexOf = function baseVectorIndexOf(value, fromIndex) {
    return indexof_1.instance.visit(this, value, fromIndex);
};
base_2.BaseVector.prototype.toArray = function baseVectorToArray() {
    return toarray_1.instance.visit(this);
};
base_2.BaseVector.prototype.getByteWidth = function baseVectorGetByteWidth() {
    return bytewidth_1.instance.visit(this.type);
};
base_2.BaseVector.prototype[Symbol.iterator] = function baseVectorSymbolIterator() {
    return iterator_1.instance.visit(this);
};
base_2.BaseVector.prototype._bindDataAccessors = bindBaseVectorDataAccessors;
// Perf: bind and assign the operator Visitor methods to each of the Vector subclasses for each Type
Object.keys(enum_1.Type)
    .map((T) => enum_1.Type[T])
    .filter((T) => typeof T === 'number')
    .filter((typeId) => typeId !== enum_1.Type.NONE)
    .forEach((typeId) => {
    const VectorCtor = vectorctor_1.instance.visit(typeId);
    VectorCtor.prototype['get'] = fn.partial1(get_1.instance.getVisitFn(typeId));
    VectorCtor.prototype['set'] = fn.partial2(set_1.instance.getVisitFn(typeId));
    VectorCtor.prototype['indexOf'] = fn.partial2(indexof_1.instance.getVisitFn(typeId));
    VectorCtor.prototype['toArray'] = fn.partial0(toarray_1.instance.getVisitFn(typeId));
    VectorCtor.prototype['getByteWidth'] = partialType0(bytewidth_1.instance.getVisitFn(typeId));
    VectorCtor.prototype[Symbol.iterator] = fn.partial0(iterator_1.instance.getVisitFn(typeId));
});
/** @ignore */
function partialType0(visit) {
    return function () { return visit(this.type); };
}
/** @ignore */
function wrapNullableGet(fn) {
    return function (i) { return this.isValid(i) ? fn.call(this, i) : null; };
}
/** @ignore */
function wrapNullableSet(fn) {
    return function (i, a) {
        if (bit_1.setBool(this.nullBitmap, this.offset + i, !(a === null || a === undefined))) {
            fn.call(this, i, a);
        }
    };
}
/** @ignore */
function bindBaseVectorDataAccessors() {
    const nullBitmap = this.nullBitmap;
    if (nullBitmap && nullBitmap.byteLength > 0) {
        this.get = wrapNullableGet(this.get);
        this.set = wrapNullableSet(this.set);
    }
}

//# sourceMappingURL=index.js.map
