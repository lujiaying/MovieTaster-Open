#coding: utf-8

import json

DoulistFile = './datas/doulist_0804_09.json'
MovieFile = './datas/movie_0804_09.json'
DoulistCorpusIdFile = DoulistFile.replace('json', 'movie_id')
DoulistCorpusNameFile = DoulistFile.replace('json', 'movie_name')

def get_movie_name_id_dict(doulist_file=DoulistFile, min_word_freq=0):
    movie_counter = {}
    with open(doulist_file) as fopen:
        for line in fopen:
            doulist_dict = json.loads(line.strip())
            for movie_name in doulist_dict['movie_names']:
                movie_name = movie_name.encode('utf8')
                if movie_name not in movie_counter:
                    movie_counter[movie_name] = 0
                movie_counter[movie_name] += 1
    movie_freq = filter(lambda _:_[1] >= min_word_freq, movie_counter.iteritems())
    movie_counter_sorted = sorted(movie_freq, key=lambda x: (-x[1], x[0]))
    movies, _ = list(zip(*movie_counter_sorted))
    movie_name_id_dict = dict(zip(movies, xrange(len(movies))))
    movie_name_id_dict['<unk>'] = len(movies)
    print('movie_name_id_dict is %d from [%s]' % (len(movie_name_id_dict), doulist_file))
    return movie_name_id_dict

def get_movie_id_name_dict(doulist_file=DoulistFile):
    movie_name_id_dict = get_movie_name_id_dict(doulist_file)
    movie_id_name_dict = dict([(_[1], _[0]) for _ in movie_name_id_dict.iteritems()])
    print('movie_id_name_dict is %d from [%s]' % (len(movie_id_name_dict), doulist_file))
    return movie_id_name_dict

def process2corpus():
    movie_name_id_dict = get_movie_name_id_dict()
    print('total movie is %d from [%s], [%s]' % (len(movie_name_id_dict), DoulistFile, MovieFile))
    unk_id = 0
    with open(DoulistFile) as fopen, open(DoulistCorpusNameFile, 'w') as fwrite, open(DoulistCorpusIdFile, 'w') as fwrite_1:
        for line in fopen:
            doulist_dict = json.loads(line.strip())
            doulist_movies = [_.encode('utf8') for _ in doulist_dict['movie_names']]
            doulist_movie_ids = [str(movie_name_id_dict[_]) for _ in doulist_movies]
            fwrite.write('%s\n' % ('\t'.join(doulist_movies)))
            fwrite_1.write('%s\n' % (' '.join(doulist_movie_ids)))

def reader_creator(movie_dict, file_name=DoulistCorpusNameFile, ngram=4):
    def reader():
        with open(file_name) as fopen:
            for line in fopen:
                line_list = line.strip().split('\t')
                movie_ids = [movie_dict.get(_, movie_dict['<unk>']) for _ in line_list]
                if len(movie_ids) >= ngram:
                    for i in range(ngram, len(movie_ids) + 1):
                        yield tuple(movie_ids[i-ngram : i])
    return reader

def reader_creator_filter(movie_dict, file_name=DoulistCorpusNameFile, ngram=4):
    def reader():
        with open(file_name) as fopen:
            for line in fopen:
                line_list = line.strip().split('\t')
                movie_ids = [movie_dict[_] for _ in line_list if _ in movie_dict]
                if len(movie_ids) >= ngram:
                    for i in range(ngram, len(movie_ids) + 1):
                        yield tuple(movie_ids[i-ngram : i])
    return reader

def itemshuffle_reader_creator(movie_dict, file_name=DoulistCorpusNameFile, ngram=4):
    import random

    def reader():
        with open(file_name) as fopen:
            for line in fopen:
                line_list = line.strip().split('\t')
                movie_ids = [movie_dict.get(_, movie_dict['<unk>']) for _ in line_list]
                random.shuffle(movie_ids)
                if len(movie_ids) >= ngram:
                    for i in range(ngram, len(movie_ids) + 1):
                        yield tuple(movie_ids[i-ngram : i])
    return reader

def shuffle(reader, buf_size):
    """
    Creates a data reader whose data output is shuffled.

    Output from the iterator that created by original reader will be
    buffered into shuffle buffer, and then shuffled. The size of shuffle buffer
    is determined by argument buf_size.

    :param reader: the original reader whose output will be shuffled.
    :type reader: callable
    :param buf_size: shuffle buffer size.
    :type buf_size: int

    :return: the new reader whose output is shuffled.
    :rtype: callable
    """
    import random
    def data_reader():
        buf = []
        for e in reader():
            buf.append(e)
            if len(buf) >= buf_size:
                random.shuffle(buf)
                for b in buf:
                    yield b
                buf = []

        if len(buf) > 0:
            random.shuffle(buf)
            for b in buf:
                yield b

    return data_reader


if __name__ == '__main__':
    process2corpus()
