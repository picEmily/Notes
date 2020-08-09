# python编译
GIL在对线程/多进程对python效率的影响
https://blog.csdn.net/i2cbus/article/details/23555063

https://baijiahao.baidu.com/s?id=1618495304088415793&wfr=spider&for=pc

http://baijiahao.baidu.com/s?id=1596285609890190878&wfr=spider&for=pc

# JIT
https://www.ibm.com/developerworks/cn/java/j-lo-just-in-time/index.html

这里是用java解释的，但是python原理应该差不多（python的cpython解释器无法jit，pypy才可以）

要点总结
- java源代码先通过javac编译成字节码（byte code），再通过jvm逐句**解释**成机器码执行。
- jvm中jit判断是否是**热点代码**（hot spot），如果是则直接将字节码编译成机器码，并且保存供以后使用。