# Java中的13个原子操作类

多线程同时更新一个变量
- ``synchronized``
- ``java.util.concurrent.atomic``
    - 使用 ``Unsafe`` 使用的**包装类**
    - 基本类型,数组,引用和属性(field)


# 原子更新基本类型

```java
/*
* 只提供了三种基本类型
* AtomicBoolean   // 原子更新布尔类型。
* AtomicInteger   // 原子更新整型。
* AtomicLong      // 原子更新长整型。
* 
* 其他基本类型 char float double 可以自己通过 Unsafe 实现
* Unsafe 提供三种 CAS 方法
*/


import java.util.concurrent.atomic.AtomicInteger;

public class AtomicIntegerTest {
    static AtomicInteger ai = new AtomicInteger(1);
    public static void main(String[] args) {
        System.out.println(ai.getAndIncrement());
        System.out.println(ai.get());
    }
}

/*
* 方法
* int addAndGet(int delta)                         相加并返回结果
* boolean compareAndSet(int expect,int update)    CAS
* int getAndIncrement()                            +=1 返回自增前的值
* void lazySet(int newValue)                       设置成新值
*/

// 通过 unsafe cas 实现以上的方法
public final int getAndIncrement() {
    for (;;) {
        int current = get();
        int next = current + 1;
        if (compareAndSet(current, next))
            return current;
        }
    }
        
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
}

```

# 原子更新数组

```java
/*
* 只提供了三种
* AtomicIntegerArray：原子更新整型数组里的元素。
* AtomicLongArray：原子更新长整型数组里的元素。
* AtomicReferenceArray：原子更新引用类型数组里的元素。
*/

/*
* 方法
* int addAndGet（int i,int delta）：以原子方式将输入值与数组中索引i的元素相加。
* boolean compareAndSet（int i,int expect,int update）
*/

public class AtomicIntegerArrayTest {        
    static int[] value = new int[] { 1, 2 };       
    static AtomicIntegerArray ai = new AtomicIntegerArray(value); // 传的不是引用,应该是浅复制
    
    public static void main(String[] args) {                
        ai.getAndSet(0, 3);                
        System.out.println(ai.get(0));  // 3                
        System.out.println(value[0]);   // 1        
        } 
    }
```

# 原子更新引用类型

```java
/*
* 
* AtomicReference 原子更新引用类型
* AtomicReferenceFieldUpdater 原子更新引用类型里的字段
* AtomicMarkableReference：原子更新带有标记位的引用类型。可以原子更新一个布尔类型的标记位和引用类型。
*/

public class AtomicReferenceTest {
    public static AtomicReference<user> atomicUserRef = new AtomicReference<user>();

    public static void main(String[] args) {
        User user = new User("conan", 15);
        atomicUserRef.set(user);                // atomicUserRef 包装了 user对象
        User updateUser = new User("Shinichi", 17);
        atomicUserRef.compareAndSet(user, updateUser);
        System.out.println(atomicUserRef.get().getName());
        System.out.println(atomicUserRef.get().getOld());
    }

    static class User {
        private String name;
        public User(String name, int old) {
            this.name = name;
            this.old = old;
        }

        public String getName() {
            return name;
        }

        public int getOld() {
            return old;
        }
    } 
}

```

# 原子更新字段类

- 原子地更新类里的某个字段  
- 必须使用静态方法 ``newUpdater()`` 创建一个更新器，设置想要更新地类和属性
- 更新类的字段（属性）必须使用 ``public volatile`` 修饰符

```java
/*
* AtomicIntegerFieldUpdater：原子更新整型的字段的更新器。
* AtomicLongFieldUpdater：原子更新长整型字段的更新器。
* AtomicStampedReference：原子更新带有版本号的引用类型。该类将整数值与引用关联起 来,可用于原子的更新数据和数据的版本号,可以解决使用CAS进行原子更新时可能出现的 ABA问题
*/

public class AtomicIntegerFieldUpdaterTest {
    // 创建原子更新器,并设置需要更新的对象类和对象的属性
    private static AtomicIntegerFieldUpdater<User> a = AtomicIntegerFieldUpdater.newUpdater(User.class, "old");
    
    public static void main(String[] args) {
        // 设置柯南的年龄是10岁
        User conan = new User("conan", 10);
        // 柯南长了一岁,但是仍然会输出旧的年龄
        System.out.println(a.getAndIncrement(conan));   // 10
        // 输出柯南现在的年龄
        System.out.println(a.get(conan));               // 11
    }
    
    public static class User {
        private String name;
        public volatile int old;                        // public volatile
        
        public User(String name, int old) {
            this.name = name;
            this.old = old;
        }
        
        public String getName() {
            return name;
        }
        
        public int getOld() {
            return old;
        }
    }
}

```
