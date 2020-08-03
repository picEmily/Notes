# 设计表
设计教务系统database

table student：
- s_id
- s_name
- s_sex

table Course:
- c_id
- c_name
- t_id

table Teacher:
- t_id
- t_name

table Score:
- s_id
- c_id
- score

table Total: (may be more redundant)
- s_id
- c_id
- t_id
- score

> 涉及到join 
- inner join = join
- outer join
- left/right join

![](https://www.runoob.com/wp-content/uploads/2019/01/sql-join.png)

# 常见例题
most know!
- where
- join...having
- 聚合函数 group by
- in/not in

**顺序**
from (on join) where (group by having) select (distinct) order by (desc) limit




