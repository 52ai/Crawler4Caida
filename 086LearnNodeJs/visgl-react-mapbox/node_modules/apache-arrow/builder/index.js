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
exports.DenseUnionBuilder = exports.SparseUnionBuilder = exports.UnionBuilder = exports.StructBuilder = exports.MapBuilder = exports.FixedSizeListBuilder = exports.ListBuilder = exports.BinaryBuilder = exports.Utf8Builder = exports.IntervalYearMonthBuilder = exports.IntervalDayTimeBuilder = exports.IntervalBuilder = exports.TimestampNanosecondBuilder = exports.TimestampMicrosecondBuilder = exports.TimestampMillisecondBuilder = exports.TimestampSecondBuilder = exports.TimestampBuilder = exports.TimeNanosecondBuilder = exports.TimeMicrosecondBuilder = exports.TimeMillisecondBuilder = exports.TimeSecondBuilder = exports.TimeBuilder = exports.Uint64Builder = exports.Uint32Builder = exports.Uint16Builder = exports.Uint8Builder = exports.Int64Builder = exports.Int32Builder = exports.Int16Builder = exports.Int8Builder = exports.IntBuilder = exports.Float64Builder = exports.Float32Builder = exports.Float16Builder = exports.FloatBuilder = exports.FixedSizeBinaryBuilder = exports.DictionaryBuilder = exports.DecimalBuilder = exports.DateMillisecondBuilder = exports.DateDayBuilder = exports.DateBuilder = exports.NullBuilder = exports.BoolBuilder = exports.Builder = void 0;
/** @ignore */
var builder_1 = require("../builder");
Object.defineProperty(exports, "Builder", { enumerable: true, get: function () { return builder_1.Builder; } });
var bool_1 = require("./bool");
Object.defineProperty(exports, "BoolBuilder", { enumerable: true, get: function () { return bool_1.BoolBuilder; } });
var null_1 = require("./null");
Object.defineProperty(exports, "NullBuilder", { enumerable: true, get: function () { return null_1.NullBuilder; } });
var date_1 = require("./date");
Object.defineProperty(exports, "DateBuilder", { enumerable: true, get: function () { return date_1.DateBuilder; } });
Object.defineProperty(exports, "DateDayBuilder", { enumerable: true, get: function () { return date_1.DateDayBuilder; } });
Object.defineProperty(exports, "DateMillisecondBuilder", { enumerable: true, get: function () { return date_1.DateMillisecondBuilder; } });
var decimal_1 = require("./decimal");
Object.defineProperty(exports, "DecimalBuilder", { enumerable: true, get: function () { return decimal_1.DecimalBuilder; } });
var dictionary_1 = require("./dictionary");
Object.defineProperty(exports, "DictionaryBuilder", { enumerable: true, get: function () { return dictionary_1.DictionaryBuilder; } });
var fixedsizebinary_1 = require("./fixedsizebinary");
Object.defineProperty(exports, "FixedSizeBinaryBuilder", { enumerable: true, get: function () { return fixedsizebinary_1.FixedSizeBinaryBuilder; } });
var float_1 = require("./float");
Object.defineProperty(exports, "FloatBuilder", { enumerable: true, get: function () { return float_1.FloatBuilder; } });
Object.defineProperty(exports, "Float16Builder", { enumerable: true, get: function () { return float_1.Float16Builder; } });
Object.defineProperty(exports, "Float32Builder", { enumerable: true, get: function () { return float_1.Float32Builder; } });
Object.defineProperty(exports, "Float64Builder", { enumerable: true, get: function () { return float_1.Float64Builder; } });
var int_1 = require("./int");
Object.defineProperty(exports, "IntBuilder", { enumerable: true, get: function () { return int_1.IntBuilder; } });
Object.defineProperty(exports, "Int8Builder", { enumerable: true, get: function () { return int_1.Int8Builder; } });
Object.defineProperty(exports, "Int16Builder", { enumerable: true, get: function () { return int_1.Int16Builder; } });
Object.defineProperty(exports, "Int32Builder", { enumerable: true, get: function () { return int_1.Int32Builder; } });
Object.defineProperty(exports, "Int64Builder", { enumerable: true, get: function () { return int_1.Int64Builder; } });
Object.defineProperty(exports, "Uint8Builder", { enumerable: true, get: function () { return int_1.Uint8Builder; } });
Object.defineProperty(exports, "Uint16Builder", { enumerable: true, get: function () { return int_1.Uint16Builder; } });
Object.defineProperty(exports, "Uint32Builder", { enumerable: true, get: function () { return int_1.Uint32Builder; } });
Object.defineProperty(exports, "Uint64Builder", { enumerable: true, get: function () { return int_1.Uint64Builder; } });
var time_1 = require("./time");
Object.defineProperty(exports, "TimeBuilder", { enumerable: true, get: function () { return time_1.TimeBuilder; } });
Object.defineProperty(exports, "TimeSecondBuilder", { enumerable: true, get: function () { return time_1.TimeSecondBuilder; } });
Object.defineProperty(exports, "TimeMillisecondBuilder", { enumerable: true, get: function () { return time_1.TimeMillisecondBuilder; } });
Object.defineProperty(exports, "TimeMicrosecondBuilder", { enumerable: true, get: function () { return time_1.TimeMicrosecondBuilder; } });
Object.defineProperty(exports, "TimeNanosecondBuilder", { enumerable: true, get: function () { return time_1.TimeNanosecondBuilder; } });
var timestamp_1 = require("./timestamp");
Object.defineProperty(exports, "TimestampBuilder", { enumerable: true, get: function () { return timestamp_1.TimestampBuilder; } });
Object.defineProperty(exports, "TimestampSecondBuilder", { enumerable: true, get: function () { return timestamp_1.TimestampSecondBuilder; } });
Object.defineProperty(exports, "TimestampMillisecondBuilder", { enumerable: true, get: function () { return timestamp_1.TimestampMillisecondBuilder; } });
Object.defineProperty(exports, "TimestampMicrosecondBuilder", { enumerable: true, get: function () { return timestamp_1.TimestampMicrosecondBuilder; } });
Object.defineProperty(exports, "TimestampNanosecondBuilder", { enumerable: true, get: function () { return timestamp_1.TimestampNanosecondBuilder; } });
var interval_1 = require("./interval");
Object.defineProperty(exports, "IntervalBuilder", { enumerable: true, get: function () { return interval_1.IntervalBuilder; } });
Object.defineProperty(exports, "IntervalDayTimeBuilder", { enumerable: true, get: function () { return interval_1.IntervalDayTimeBuilder; } });
Object.defineProperty(exports, "IntervalYearMonthBuilder", { enumerable: true, get: function () { return interval_1.IntervalYearMonthBuilder; } });
var utf8_1 = require("./utf8");
Object.defineProperty(exports, "Utf8Builder", { enumerable: true, get: function () { return utf8_1.Utf8Builder; } });
var binary_1 = require("./binary");
Object.defineProperty(exports, "BinaryBuilder", { enumerable: true, get: function () { return binary_1.BinaryBuilder; } });
var list_1 = require("./list");
Object.defineProperty(exports, "ListBuilder", { enumerable: true, get: function () { return list_1.ListBuilder; } });
var fixedsizelist_1 = require("./fixedsizelist");
Object.defineProperty(exports, "FixedSizeListBuilder", { enumerable: true, get: function () { return fixedsizelist_1.FixedSizeListBuilder; } });
var map_1 = require("./map");
Object.defineProperty(exports, "MapBuilder", { enumerable: true, get: function () { return map_1.MapBuilder; } });
var struct_1 = require("./struct");
Object.defineProperty(exports, "StructBuilder", { enumerable: true, get: function () { return struct_1.StructBuilder; } });
var union_1 = require("./union");
Object.defineProperty(exports, "UnionBuilder", { enumerable: true, get: function () { return union_1.UnionBuilder; } });
Object.defineProperty(exports, "SparseUnionBuilder", { enumerable: true, get: function () { return union_1.SparseUnionBuilder; } });
Object.defineProperty(exports, "DenseUnionBuilder", { enumerable: true, get: function () { return union_1.DenseUnionBuilder; } });
const enum_1 = require("../enum");
const utf8_2 = require("./utf8");
const builder_2 = require("../builder");
const set_1 = require("../visitor/set");
const builderctor_1 = require("../visitor/builderctor");
/** @nocollapse */
builder_2.Builder.new = newBuilder;
function newBuilder(options) {
    const type = options.type;
    const builder = new (builderctor_1.instance.getVisitFn(type)())(options);
    if (type.children && type.children.length > 0) {
        const children = options['children'] || [];
        const defaultOptions = { 'nullValues': options['nullValues'] };
        const getChildOptions = Array.isArray(children)
            ? ((_, i) => children[i] || defaultOptions)
            : (({ name }) => children[name] || defaultOptions);
        type.children.forEach((field, index) => {
            const { type } = field;
            const opts = getChildOptions(field, index);
            builder.children.push(newBuilder({ ...opts, type }));
        });
    }
    return builder;
}
Object.keys(enum_1.Type)
    .map((T) => enum_1.Type[T])
    .filter((T) => typeof T === 'number' && T !== enum_1.Type.NONE)
    .forEach((typeId) => {
    const BuilderCtor = builderctor_1.instance.visit(typeId);
    BuilderCtor.prototype._setValue = set_1.instance.getVisitFn(typeId);
});
utf8_2.Utf8Builder.prototype._setValue = set_1.instance.visitBinary;

//# sourceMappingURL=index.js.map
