// learn es6

{
    let a = 10;
    var b =1;

}
console.log(b);
// console.log(a); 报错，let声明的变量只在它所在的代码块有效

// 字符串的遍历器接口

for (let codePoint of 'foo') {
    console.log(codePoint)
}

// 类

class Foo {
    constructor()  {
        console.log("run foo constructor.");
    }
}

class Bar extends Foo {
    constructor() {
        super();
        console.log("run Bar constructor.");
    }
}
// ES6继承机制，继承在前，实例在后，这也就意味着新建子类实例，父类的构造函数必定先运行一次
const bar = new Bar();


