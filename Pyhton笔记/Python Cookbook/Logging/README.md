logging库由logger，handler，filter，formater四个部分组成
- logger  Instances of the Logger class represent a single logging channel. A
    "logging channel" indicates an area of an application. Exactly how an
    "area" is defined is up to the application developer. Since an
    application can have any number of areas, logging channels are identified
    by a unique string. Application areas can be nested (e.g. an area
    of "input processing" might include sub-areas "read CSV files", "read
    XLS files" and "read Gnumeric files"). To cater for this natural nesting,
    channel names are organized into a namespace hierarchy where levels are
    separated by periods, much like the Java or Python package namespace. So
    in the instance given above, channel names might be "input" for the upper
    level, and "input.csv", "input.xls" and "input.gnu" for the sub-levels.
    There is no arbitrary limit to the depth of nesting.
- handler是让我们选择日志的输出地方，如：控制台，文件，邮件发送等，一个logger添加多个handler；
- filter是给用户提供更加细粒度的控制日志的输出内容；
- formater用户格式化输出日志的信息。

python中配置logging有三种方式
- 第一种：基础配置，logging.basicConfig(filename="config.log",filemode="w",format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",level=logging.INFO)。
- 第二种：使用配置文件的方式配置logging,使用logging.config.fileConfig(filename,defaults=None,disable_existing_loggers=Ture )函数来读取配置文件。
- 第三种：使用一个字典方式来写配置信息，然后使用logging.config.dictConfig(dict,defaults=None, disable_existing_loggers=Ture )函数来完成logging的配置.
- 第四种：使用logger类，可以通过 logging.getLogger(__name__)