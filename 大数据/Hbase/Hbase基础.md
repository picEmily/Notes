参考：https://developer.ibm.com/zh/articles/ba-cn-bigdata-hbase/

# Hbase 是什么

**基本认识**

- 分布式文件系统：HDFS
- 分布式计算框架：Hadoop（重要技术：MapReduce）

Hbase 是基于 Hadoop 的分布式数据库，底层依旧使用 HDFS 作为存储。

## 区别传统数据库

- Hbase 不是关系型数据库，Hbase 是 KV 结构（Key是RowKey+CF+ColumnKey，Value是Cell Value）
- 特点是 **分布式，索引为 Row-Key，数据量PB级别**

|              | HBase                                                        | RDBMS                            |
| :----------- | :----------------------------------------------------------- | :------------------------------- |
| 硬件架构     | 类似于 Hadoop 的分布式集群，硬件成本低廉                     | 传统的多核系统，硬件成本昂贵     |
| 容错性       | 由软件架构实现，由于由多个节点组成，所以不担心一点或几点宕机 | 一般需要额外硬件设备实现 HA 机制 |
| 数据库大小   | PB                                                           | GB、TB                           |
| 数据排布方式 | **稀疏的、分布的多维的 Map**                                 | 以行和列组织                     |
| 数据类型     | Bytes                                                        | 丰富的数据类型                   |
| 事物支持     | ACID 只支持单个 Row 级别                                     | 全面的 ACID 支持，对 Row 和表    |
| 查询语言     | 只支持 Java API （除非与其他框架一起使用，如 Phoenix、Hive） | SQL                              |
| 索引         | **只支持 Row-key**，除非与其他技术一起应用，如 Phoenix、Hive | 支持                             |
| 吞吐量       | 百万查询/每秒                                                | 数千查询/每秒                    |

# Hbase 的数据

重要组成部分：

- Column Family（CF）
  - 列族下面可以有几个列
  - 一般一张表的 列族<3
- Column Key / Qualifier
- Row-Key
  - 起到索引的作用
- Time Stamp
  - 用于 多版本控制
- Cell：Row-Key+Column Family+Qualifier 共同确认
  - 张，三，26，男 都是 cell

## 逻辑存储模型

这完全是个逻辑模型，为了方便从关系型数据库转变思路

| Row Key |   Column Family1   |                    |    Column Family2    |                      | Time Stamp |
| :-----: | :----------------: | :----------------: | :------------------: | :------------------: | :--------: |
|         | **Column Key**: 姓 | **Column Key**: 名 | **Column Key**: 年龄 | **Column Key**: 性别 |            |
|   001   |         张         |         三         |          26          |          男          |     T1     |
|   002   |         李         |         四         |          30          |          女          |     T2     |

另一种画法，是一个意思，更能体现 Hbase 所谓的 **列存储**（cell value 是竖着排布的）

这样画也更接近物理上实际存储方式： Row-Key+Column Family+Qualifier 共同确定 cell value

| Row Key | Column Family: Column Key | Time Stamp | Cell |
| ------- | ------------------------- | ---------- | ---- |
| 001     | Column Family1：姓        | T1         | 张   |
| 001     | Column Family2：年龄      | T1         | 26   |
| 002     | Column Family1：姓        | T2         | 李   |
| 002     | Column Family2：年龄      | T2         | 30   |

## 物理存储模型

- Region：HBase 并行的基本单元
  - 每个 Region 只存储一个 CF，并且按照 Row 来切割
  - Region 的大小有上限，达到上限就会分裂
  - Store+MemStore：内存中有序的数据，MemStore 满了就持久化到 HFile（HDFS 层）
- Region Server：管理多个 Region
- Master：Master 分配 Region 到 Region Server，Master 和 Region Server 通过 ZooKeeper 沟通
- Log：WAL 模式

注意：存的都是 Bytes

<img src="C:\Users\wangd\Desktop\Hbase\Hbase架构.png" style="zoom: 33%;" />

补充：HFile 的结构

<img src="C:\Users\wangd\Desktop\Hbase\Hfile结构.png" style="zoom:30%;" />

- 图中画的是一个组 Block，每个 Block 是由一个 Header 和多个 Key-Value 的键值对组成
- 这一组 Block 的索引在 Trailer 中