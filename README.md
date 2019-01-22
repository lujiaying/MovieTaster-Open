# MovieTaster-Open

A movie recommend project based on Item2vec.

Reference: 
- Barkan, Oren, and Noam Koenigstein. "Item2vec: neural item embedding for collaborative filtering." Machine Learning for Signal Processing (MLSP), 2016 IEEE 26th International Workshop on. IEEE, 2016.
- JayveeHe, https://github.com/JayveeHe/MusicTaster. Github.

[Demo>](https://movietaster.leanapp.cn/movies/)

<img src="/recommend_multiple.jpg" />

More details for this project, plese refer to [blog>](https://lujiaying.github.io/posts/2017/08/MovieTaster/) or [zhihu>](https://zhuanlan.zhihu.com/p/28491088)

## Project Struct
- datas:  to store corpus
- models: to store item vectors for movies
- utils: a collection of tool functions


## Usage

0. Compile [fasttext](https://github.com/facebookresearch/fastText) under root of the project

1. Process corpus, the data file would be generated under ```./datas/```.

```
$ cd datas && tar -xzvf corpus.tar.gz
$ cd ..
$ python utils/process.py
```

2. Train model by running fasttext. Please refer to ```./run.sh``` for other configuration.

```
$ ./fasttext skipgram -input ./datas/doulist_0804_09.movie_id -output ./models/fasttext_model_0804_09_skipgram -minCount 5 -epoch 50 -neg 100
```

3. Here's a result from the default configuration.

```
$ python utils/eval.py
movie_name_id_dict is 130206 from [./datas/doulist_0804_09.json]
movie_name_id_dict is 130206 from [./datas/doulist_0804_09.json]
movie_id_name_dict is 130206 from [./datas/doulist_0804_09.json]
[2017-08-18 07:52:53,579][pid:22831] eval.topk_like: INFO: [1210]小时代 top 5 likes:
[2017-08-18 07:52:54,149][pid:22831] eval.topk_like: INFO: [2396]小时代2：青木时代 0.820323
[2017-08-18 07:52:54,149][pid:22831] eval.topk_like: INFO: [3387]分手合约 0.606063
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [4087]不二神探 0.604207
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [3839]天台爱情 0.601879
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [821]致我们终将逝去的青春 0.600836
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [144]倩女幽魂 top 5 likes:
[2017-08-18 07:52:54,690][pid:22831] eval.topk_like: INFO: [2719]倩女幽魂3：道道道 0.685621
[2017-08-18 07:52:54,690][pid:22831] eval.topk_like: INFO: [1812]倩女幽魂2：人间道 0.681594
[2017-08-18 07:52:54,691][pid:22831] eval.topk_like: INFO: [466]胭脂扣 0.678032
[2017-08-18 07:52:54,691][pid:22831] eval.topk_like: INFO: [261]青蛇 0.671541
[2017-08-18 07:52:54,692][pid:22831] eval.topk_like: INFO: [156]东邪西毒 0.664057
[2017-08-18 07:52:54,692][pid:22831] eval.topk_like: INFO: [2602]悟空传 top 5 likes:
[2017-08-18 07:52:55,253][pid:22831] eval.topk_like: INFO: [5648]闪光少女 0.671337
[2017-08-18 07:52:55,253][pid:22831] eval.topk_like: INFO: [2189]绣春刀II：修罗战场 0.646861
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [8297]逆时营救 0.634753
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [12571]京城81号Ⅱ 0.625549
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [10545]父子雄兵 0.623032
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [56]美国往事 top 5 likes:
[2017-08-18 07:52:55,789][pid:22831] eval.topk_like: INFO: [18]天堂电影院 0.756449
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [14]辛德勒的名单 0.737502
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [17]教父 0.735216
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [69]闻香识女人 0.734119
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [42]西西里的美丽传说 0.732334
[2017-08-18 07:52:55,791][pid:22831] eval.topk_like: INFO: [2644]战狼2 top 5 likes:
[2017-08-18 07:52:56,346][pid:22831] eval.topk_like: INFO: [1456]大护法 0.612700
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [2107]战狼 0.580637
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [2602]悟空传 0.580365
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [9941]建军大业 0.575422
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [19040]阿唐奇遇 0.573613
```

------------------------

# MovieTaster-Open

使用Item2Vec做电影推荐

参考: 
- Barkan, Oren, and Noam Koenigstein. "Item2vec: neural item embedding for collaborative filtering." Machine Learning for Signal Processing (MLSP), 2016 IEEE 26th International Workshop on. IEEE, 2016.
- JayveeHe, https://github.com/JayveeHe/MusicTaster. Github.

[Demo>](https://movietaster.leanapp.cn/movies/)

<img src="/recommend_multiple.jpg" />

[原理详情请参考>](https://lujiaying.github.io/posts/2017/08/MovieTaster/)

## 目录结构
- datas:  存放语料
- models: 存放电影向量
- utils: 工具类，包括生成推荐电影列表等


## 使用说明

0. 在根目录下载并编译[fasttext](https://github.com/facebookresearch/fastText)

1. 处理语料。结束后将在```./datas/```下生成fasttext所需要的格式

```
$ cd datas && tar -xzvf corpus.tar.gz
$ cd ..
$ python utils/process.py
```

2. 参考```./run.sh```中生成词向量的参数配置，任选一个。

```
$ ./fasttext skipgram -input ./datas/doulist_0804_09.movie_id -output ./models/fasttext_model_0804_09_skipgram -minCount 5 -epoch 50 -neg 100
```

3. 查看模型效果

```
$ python utils/eval.py
movie_name_id_dict is 130206 from [./datas/doulist_0804_09.json]
movie_name_id_dict is 130206 from [./datas/doulist_0804_09.json]
movie_id_name_dict is 130206 from [./datas/doulist_0804_09.json]
[2017-08-18 07:52:53,579][pid:22831] eval.topk_like: INFO: [1210]小时代 top 5 likes:
[2017-08-18 07:52:54,149][pid:22831] eval.topk_like: INFO: [2396]小时代2：青木时代 0.820323
[2017-08-18 07:52:54,149][pid:22831] eval.topk_like: INFO: [3387]分手合约 0.606063
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [4087]不二神探 0.604207
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [3839]天台爱情 0.601879
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [821]致我们终将逝去的青春 0.600836
[2017-08-18 07:52:54,150][pid:22831] eval.topk_like: INFO: [144]倩女幽魂 top 5 likes:
[2017-08-18 07:52:54,690][pid:22831] eval.topk_like: INFO: [2719]倩女幽魂3：道道道 0.685621
[2017-08-18 07:52:54,690][pid:22831] eval.topk_like: INFO: [1812]倩女幽魂2：人间道 0.681594
[2017-08-18 07:52:54,691][pid:22831] eval.topk_like: INFO: [466]胭脂扣 0.678032
[2017-08-18 07:52:54,691][pid:22831] eval.topk_like: INFO: [261]青蛇 0.671541
[2017-08-18 07:52:54,692][pid:22831] eval.topk_like: INFO: [156]东邪西毒 0.664057
[2017-08-18 07:52:54,692][pid:22831] eval.topk_like: INFO: [2602]悟空传 top 5 likes:
[2017-08-18 07:52:55,253][pid:22831] eval.topk_like: INFO: [5648]闪光少女 0.671337
[2017-08-18 07:52:55,253][pid:22831] eval.topk_like: INFO: [2189]绣春刀II：修罗战场 0.646861
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [8297]逆时营救 0.634753
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [12571]京城81号Ⅱ 0.625549
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [10545]父子雄兵 0.623032
[2017-08-18 07:52:55,254][pid:22831] eval.topk_like: INFO: [56]美国往事 top 5 likes:
[2017-08-18 07:52:55,789][pid:22831] eval.topk_like: INFO: [18]天堂电影院 0.756449
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [14]辛德勒的名单 0.737502
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [17]教父 0.735216
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [69]闻香识女人 0.734119
[2017-08-18 07:52:55,790][pid:22831] eval.topk_like: INFO: [42]西西里的美丽传说 0.732334
[2017-08-18 07:52:55,791][pid:22831] eval.topk_like: INFO: [2644]战狼2 top 5 likes:
[2017-08-18 07:52:56,346][pid:22831] eval.topk_like: INFO: [1456]大护法 0.612700
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [2107]战狼 0.580637
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [2602]悟空传 0.580365
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [9941]建军大业 0.575422
[2017-08-18 07:52:56,347][pid:22831] eval.topk_like: INFO: [19040]阿唐奇遇 0.573613
```
