 ./fasttext skipgram -input ./datas/doulist_0803_23.movie_id -output ./models/fasttext_model_0803_23 -minCount 2
 ./fasttext skipgram -input ./datas/doulist_0804_09.movie_id -output ./models/fasttext_model_0804_09_skipgram -minCount 5 -epoch 50 -neg 100
 ./fasttext cbow -input ./datas/doulist_0804_09.movie_id -output ./models/fasttext_model_0804_09_cbow -minCount 5 -epoch 50 -neg 100
