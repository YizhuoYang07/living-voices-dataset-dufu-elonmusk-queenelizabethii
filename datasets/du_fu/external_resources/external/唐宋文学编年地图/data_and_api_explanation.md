[知识图谱网](https://cnkgraph.com/)一直致力于构建中文领域特别是古典文史领域的知识图谱。虽然目前离最终建设目标尚远，但是也不乏一些成果。为了让本网的数据及功能够更轻松地为同行所利用，本网已开发出 Web API 接口，开放所有的数据与功能，方便有兴趣的个人或机构，集成或获取本网的数据，进行研究、学习（仅限非商业用途）。

##### **数据集**

CNKGraph.Writings.xml 文件

##### 接口网址

- 开放接口网址：https://open.cnkgraph.com

##### 接口示例

- PostMan格式示例：postman 文件夹

下载以上示例并导入 PostMan 之后，可看到接口清单如下：

![img](https://cnkgraph.com/images/open/postman1.png)
![img](https://cnkgraph.com/images/open/postman2.png)
![img](https://cnkgraph.com/images/open/postman3.png)

对比网站可见，这些接口基本已经涵盖了所有数据与功能。

##### 接口说明

本网接口都是基于 RESTful 设计，易于理解，返回都是可读性比较高的 JSON 格式数据，所以在此不打算对每一个接口的输入和输出参数做详细说明。一般来说，参照 PostMan 的示例，对照网站的显示效果，便可知道各种属性的含义。作者也正在基于 OpenAPI3.1 编写YAML格式的详细接口说明，下载地址：https://open.cnkgraph.com/Api/index.yaml 目前诗文库接口的详细定义及说明已完成。其它接口的详细说明工作，还待开展，敬请留意该网址的更新。

##### 如何获得未经繁简转换的原始数据？

接口会根据 HTTP Header 中的“Accept-Language”属性值，判断是否需要在返回数据之前，把繁体汉字转成简体汉字。如果你希望系统不作此转换，直接返回原始数据，可把 Accept-Language 属性值设置成“zh-hant”。详参 PostMan 中，诗文库目录下，关于“获取特定作品，返回结果不作繁简转换”的示例。