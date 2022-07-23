# Sino-Japanese-Relations-analysis

## 项目任务

### 主线任务

1. 完成 `./target` 路径下的所有网站以及对应信息的爬取（储存为  `html` 等格式），数据分析（储存为 `csv, json` 等格式），数据可视化（热力图，词云图，基本统计数据图等等）
2. 等待语义组同学反馈，及时调整数据来源与分析要求，并且配合新的可视化需求

### 支线任务

1. 受到一字班辅导员王导的邀请，集体贡献一份 Python 小学期数据分析部分的技能文档

### **说明**

我在招募各位之前就告知大家，此项目和大一 Python 小学期几乎完全相同，从网络爬虫到数据分析，再到可视化，这就是小学期 Python 第一周的基本工作内容。

在招募大家之前，我承诺过需要会帮助大家完整掌握这三部分，且能够优雅地在平时的工作里使用。在几天前，王导联系我，希望科协能否提供一份为一字班小学期同学的帮助指南，以避免课程过度 fly bitch。相信大家都知道，本人之前在技能文档项目贡献过我的 [OOP 笔记](https://docs.net9.org/languages/c-oop/)。

相应的，本次项目需要大家完成自己负责部分的对应课程笔记，然后在本仓库开源，在 8 月 1 日前面向计算机系一字班开源，以作为一字班同学小学期预习的参考资料。

可能大家之前没有参与过类似的项目，这里我阐明下项目的意义：

1. 培养开源精神，实际上我们所接触的互联网世界就是基于无数前人和同辈的开源精神构建而成。如果我们也想贡献开源社区，也希望成为伟大的计算机科学家或者计算机技术专家，养成良好的开源精神是必要的
2. 助力养成团队协作，查阅资料自我学习和编写技能文档的习惯。实际上，如果各位去大厂面试，附带上自己的技术文档博客往往比空洞地阐明自己在各类课程上取得的成绩更加有价值
3. 帮助你的同学们，留名青史。虽然说留名青史很夸张，然而大家自然理解，计算机系的 cracker 和 by-pass 都是无数的前人留下的历史丰碑。虽然目前计算机系的课程质量任然堪忧，大一小学期尤其如此，但是我们每贡献一次开源资料，都会为计算机系课程质量提升留下不可磨灭的贡献

## 相应任务分工

```shell
.
├── LICENSE
├── README.md
├── crawler
├── docs
│   ├── DS_tutorial.pdf
│   ├── crawler
│   ├── soup
│   │   ├── Numerical\ Python.ipynb
│   │   ├── Pandas.ipynb
│   │   └── Python\ Advanced\ Topics.ipynb
│   └── visualize
│       ├── Matplotlib\ Original.ipynb
│       └── Matplotlib.ipynb
├── soup
├── target
│   ├── website_Chinese.xlsx
│   └── website_Janpanese.xlsx
└── visualize

8 directories, 10 files
```

`crawler` 为爬虫工作文件夹 @QuentinHsuow，`soup` 为解析文件夹 @caigouyige，`visualize` 为可视化文件夹 @luohaowen2003。`docs` 为按照王导想法需要完成的笔记文件夹，请按照各自的主线任务完成对应部分的支线任务。

在 `docs` 文件夹下存放了一些原始文件，`DS_tutorial.pdf` 为我暑培课程的参考书，我也强烈建议各位参考。`crawler` 文件夹请参考 `lambda` 的暑培讲义，编写一份 Jupyter 文档。而 `soup` 文件夹，按照之前的规划，请 @caigouyige 把自己翻译的 Pandas 和 BS4 文档 merge 进去。最后，`visualize` 文件夹，请 @luohaowen2003 参考 `DS_tutorial.pdf` 把 `Matplotlib.ipynb` 翻译完全。

翻译完整后的文件，会经过科协网络部技能文档组审核 @c7w，对于原创性较高的文档给予经济回报。

## DDL

### 爬虫部分

我的建议是先爬虫，边爬边修改 lambda 的暑培讲义，全部网页给出 25 日的 DDL。注意，全部网页是指所有的中日网站，实际上爬虫是离散化的，每爬取一点，请立刻利用清华云盘传给解析的同学，用作分析和后续可视化。

笔记的 DDL 是 26 日，之后会加以审核。

如果需要购买 IP 池，请请教 lambda，并且尽量开发票。

### 解析部分

我的建议是，完成手头的所有笔记后，再开始解析也不迟。目前 @caigouyige 只剩下了 BS4 文档。注意，解析的要求参考 `target` 文件夹。

文档 DDL 定于 26 日，解析 DDL 定于 28 日。请合理保存所有的解析源文件和解析后的所有格式，并存放在清华云盘。

### 可视化

可视化请翻译完所有的笔记后等待甲方对可视化的要求。另外，可视化部分主要的工作集中在学期中答辩之前，预期工作量 10h。

笔记 DDL 为 26 日。

## 开发规范

1. 参考我在暑培课程的讲义，注意代码风格和鲁棒性等等要求
2. 开设分支进行开发，禁止直接修改 `main`

## 参考资料

[Analysis-of-National-Branding-Strategy-from-China-Japan-Media](https://github.com/zhaochenyang20/Analysis-of-National-Branding-Strategy-from-China-Japan-Media)

