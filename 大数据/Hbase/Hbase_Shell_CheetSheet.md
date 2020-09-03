# Start Hbase

```
hbase shell
```

 # General commands

```
# server 数量，活着的 server，负载
status
# 可以附加参数, Hbase 都是单引号
status 'summary'
status 'simple'
status 'detailed'

# Version
version

# Help
table_help
table_help ( scan, drop, get, put, disable, etc.)

# the current Hbase infomation
whoami
```

# Table Management

```
create <table name>, <column familyname>
list										# all tables presenting in HBase
describe <table name>						# describe the table: CF, filters, version...

enable <table name>
is_enabled <table name>

disable <table name>						# If table needs to be deleted or dropped, it has to disable first
disable_all <"matching regex">
drop <table name>							# drop and delete???
drop_all <"matching regex">

alter <tablename>, NAME => <column familyname>, VERSIONS => 5	# alters the column family schema.
alter_status 'education'					# get the status after calling alter	
	
show_filters
```

# Data Manipulation

```
count <tablename>, CACHE => 1000			# Current count is shown per every 1000 rows by default
put <'tablename'>,<'rowname'>,<'columnvalue'>,<'value'>

delete <'tablename'>,<'row name'>,<'column name'>
deleteall <'tablename'>, <'rowname'>

get <'tablename'>, <'rowname'>, {< Additional parameters>}
scan <'tablename'>, {Optional parameters}
```

## Examples of scan

```
scan '.META.', {COLUMNS => 'info:regioninfo'}
scan 'guru99', {COLUMNS => ['c1', 'c2'], LIMIT => 10, STARTROW => '1'}
scan 'guru99', {COLUMNS => 'c1', TIMERANGE => [1303668804, 1303668904]}
scan 'guru99', {RAW => true, VERSIONS =>10}

# filter
scan 'guru99', FILTER=>"ValueFilter(=,'binary:foo')"  
```



