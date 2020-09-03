参考：

https://hbase.apache.org/apidocs/

https://www.baeldung.com/hbase

http://www.corejavaguru.com/bigdata/hbase-tutorial/hbase-java-client-api-examples

- 连接
- CRUD

注意：Hbase 里面存的都是 Bytes

# 准备工作

```java
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

Configuration config = HBaseConfiguration.create();
HTable table = new HTable(config, "FooTable");			// 表
```

如果是 Spring 的话在 Maven 中引入

```java
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-client</artifactId>
    <version>${hbase.version}</version>
</dependency>
<dependency>
     <groupId>org.apache.hbase</groupId>
     <artifactId>hbase</artifactId>
     <version>${hbase.version}</version>
</dependency>
```

# 查询

- Get 获取一条数据
- Scan 获取多条数据，还可以加 filter

## ## Get

```java
// instantiate Get class
Get g = new Get(Bytes.toBytes("row1"));

// get the Result object
Result result = table.get(g);

// read and print the result
byte [] cell_value1 = result.getValue(Bytes.toBytes("CF1"), Bytes.toBytes("CK1"));
System.out.println("cell_value1: " + Bytes.toString(cell_value1));
```

## ## Scan

```java
// instantiate the Scan class
Scan scan = new Scan();

// scan the columns
scan.addColumn(Bytes.toBytes("CF1"), Bytes.toBytes("CK1"));
scan.addColumn(Bytes.toBytes("CF2"), Bytes.toBytes("CK2"));

// get the ResultScanner
ResultScanner scanner = table.getScanner(scan);

// 写法1
for (Result result = scanner.next(); result != null; result=scanner.next()) {
    System.out.println("Found row : " + result);
}

// 写法2
for (Result result : scanner) {
    // do something
}

// with filter
// valueFilter, QualifierFilter, PrefixFilter
Filter filter1 = new PrefixFilter(row1);
Filter filter2 = new QualifierFilter(CompareOp.GREATER_OR_EQUAL, new BinaryComparator(qualifier1));
List<Filter> filters = Arrays.asList(filter1, filter2);				// 定义多个 filter 并放入一个 List 中
scan.setFilter(new FilterList(Operator.MUST_PASS_ALL, filters));	// 给 scan 实例设置 filter
 
try (ResultScanner scanner = table.getScanner(scan)) {
    for (Result result : scanner) {
        System.out.println("Found row: " + result);
    }
}

scanner.close();
```

