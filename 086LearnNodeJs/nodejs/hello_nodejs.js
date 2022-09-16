// Learning Node.JS，open a new window for future.

// for 循环基本用法
for (var i=1; i<=10; i++){
    console.log("Hello Node.JS!");
}

// for循环结合if语句
for (var i=1; i<=20; i++){
    if(i==10){
        console.log("Hello, 10!");
    }else if (i==20){
        console.log("Hello, 100!");
    }else{
        console.log("Hello, Other Numbers!")
    }
}

//for 双重for循环
var star = '';
for (var j=1;j<=3;j++){
    for(var i=1;i<=3;i++){
        star += '*';
    }
}
console.log(star)

// continue 跳出当次循环
// break 退出整个循环

// 递归

var x = 0;
function fn(){
    x++;
    console.log('Hello, Recursion！');
    if (x==3){
        return;
    }
    fn();//函数内部调用函数本身
}

fn();

// 对象

var obj = {}

// 对象属性
obj.name = "Wayne";
obj.age = "28";
obj.weight = 140;
obj.sex = "Male";

// 对象方法
obj.eat = function(){
    console.log("Wayne like eat!");
}

console.log(obj);//obj代表整个对象

// 对象的遍历

for(var k in obj){
    console.log(k, obj[k])
}
obj.eat();

// 数组

var arr1 = [12,23,34,13,5];
var sum = 0;
for (var i=0;i<arr1.length;i++){
    console.log(arr1[i])
    if (arr1[i] % 2 == 1){
        sum += arr1[i];
    }
}
console.log("The sum of odd numbers:", sum);

// for in 方式遍历数组
for (var i in arr1){
    console.log(arr1[i]);
}

arr1.push(41,42);// push函数，向数组末尾添加一个或多个元素，并返回新的长度
console.log("After push, Array new length:", arr1.length);

arr1.pop();// pop函数，删除并返回数组的最后一个元素
console.log("After pop, Array new length:", arr1.length);

// unshift函数，向数组开头添加一个或多个元素，并返回新的长度
arr1.unshift(7, 8);
console.log("After pop, Array new length:", arr1.length);

// shift函数，删除数组的第一个元素，并返回第一个元素
arr1.shift();
console.log("After shift, Array new length:", arr1.length);

// join(char)， 把数组元素（对象调用其toString()方法），使用参数作为连接符连接成字符串
arr1_string = arr1.join("*");
console.log("toString:", arr1_string)

// reverse(), 将数组逆序，与之前不同的是它会修改原数组
arr1.reverse()
console.log(arr1)

// sort(), 对数组进行排序
arr1.sort(function(a,b){
    return a-b;//从大到小
})
console.log(arr1)

// 二维数组
var arr2 = [[1,2,3],[4,5,6], [7,8,9]]
for (var i=0;i<arr2.length;i++){
    for (var j=0;j<arr2[i].length;j++){
        console.log(arr2[i][j] + " ");
    }
}

// json

var num = {
    "name": "js",
    "age":18
}

console.log(JSON.stringify(num));

var str = '{"name":"js","age":18}';
console.log(JSON.parse(str));

// let在es6里用来申明变量

let a = 10;
console.log(a)

// const在es6里用来申明常量

const PI = 3.14;
console.log(PI)

// 箭头函数

var fn1 = function(){
    console.log(1);
}

fn1();

var fn2 = ()=> {
    console.log(2);
}
fn2();

var fn3 = function(a, b){
    console.log(a+b);
}
fn3(1,2);

var fn4 = (a,b)=> {
    console.log(a+b);
    return a*b;
}
console.log(fn4(2,3));

// 解构赋值，从数组或对象中把元素或健解构出来，赋值给变量

// set 类似于数组，但它的值不会重复，可用于自动去重
var s = new Set([12,34,12,34,56]);
console.log(s);

// map 类似于对象
var m = new Map()
m.set('a', 1);//添加内容
m.set('b', 2);
console.log(m.get('a'));//获取元素
console.log(m.has('a'));//判断是否包含'a'

//闭包，在一个函数内部再定义一个函数，内部函数使用外部函数的局部变量，并且外部函数返回值是内部函数

function out1(){
    var a= 111;
    function in2(){
        return a;
    }
    return in2;
}

var f1 = out1();// f1等于in2()
var f2 = f1();//f2 等于in2的返回值，即a

// 闭包的作用就是可以在全局位置访问到局部的变量
console.log(f1);
console.log(f2);

// 内置fs模块操作文件
var ff = require('fs');

//文件写入
ff.writeFile("test.txt", "This is a test File for JS write function.", (err, data) => {
    if (err){
        console.log(err);
        return;
    }
    console.log("Write Success!");
})

//文件读取
ff.readFile("test.txt", 'utf-8', (err, data) => {
    if(err){
        console.log(err);
        return;
    }
    console.log("Read Success!");
})

