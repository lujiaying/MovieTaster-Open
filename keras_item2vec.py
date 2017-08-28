import keras
from keras.models import Sequential, Model
from keras.layers import Activation, Merge, Reshape
from keras.layers import Input, Embedding, Dense, dot
from keras.layers.core import Lambda
from keras import optimizers
from keras import backend as K
import numpy as np
import random

import utils.process as process
from utils.log_tool import data_process_logger as logger

def skipgram_model(vocab_size, embedding_dim=100, paradigm='Functional'):
    # Sequential paradigm
    if paradigm == 'Sequential':
        target = Sequential()
        target.add(Embedding(vocab_size, embedding_dim, input_length=1))
        context = Sequential()
        context.add(Embedding(vocab_size, embedding_dim, input_length=1))

        # merge the pivot and context models
        model = Sequential()
        model.add(Merge([target, context], mode='dot'))
        model.add(Reshape((1,), input_shape=(1,1)))
        model.add(Activation('sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

    # Functional paradigm
    elif paradigm == 'Functional':
        target = Input(shape=(1,), name='target')
        context = Input(shape=(1,), name='context')
        #print target.shape, context.shape
        shared_embedding = Embedding(vocab_size, embedding_dim, input_length=1, name='shared_embedding')
        embedding_target = shared_embedding(target)
        embedding_context = shared_embedding(context)
        #print embedding_target.shape, embedding_context.shape

        merged_vector = dot([embedding_target, embedding_context], axes=-1)
        reshaped_vector = Reshape((1,), input_shape=(1,1))(merged_vector)
        #print merged_vector.shape
        prediction = Dense(1, input_shape=(1,), activation='sigmoid')(reshaped_vector)
        #print prediction.shape

        model = Model(inputs=[target, context], outputs=prediction)
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

    else:
        print('paradigm error')
        return None
    

def skipgram_reader_generator(movie_dict, file_name=process.DoulistCorpusNameFile, context_window=2):
    def reader():
        vocabulary_size = len(movie_dict)
        with open(file_name) as fopen:
            for line in fopen:
                line_list = line.strip().split('\t')
                movie_ids = [movie_dict.get(_, movie_dict['<unk>']) for _ in line_list]
                for i in range(len(movie_ids)):
                    target = movie_ids[i]
                    # generate positive sample
                    context_list = []
                    j = i - context_window
                    while j <= i + context_window and j < len(movie_ids):
                        if j >= 0 and j != i:
                            context_list.append(movie_ids[j])
                            yield ((target, movie_ids[j]), 1)
                        j += 1
                    # generate negative sample
                    for _ in range(len(context_list)):
                        ne_idx = random.randrange(0, vocabulary_size)
                        while ne_idx in context_list:
                            ne_idx = random.randrange(0, vocabulary_size)
                        yield ((target, ne_idx), 0)
    return reader

def cbow_base_model(dict_size, emb_size=100, context_window_size=4):
    model = keras.models.Sequential()
    model.add(Embedding(dict_size, emb_size, 
        input_length=context_window_size,
        embeddings_initializer=keras.initializers.TruncatedNormal(mean=0.0, stddev=0.2),
        ))
    model.add(Lambda(lambda x: K.mean(x, axis=1), output_shape=(emb_size,)))
    model.add(Dense(dict_size))
    model.add(Activation('softmax')) # TODO: use nce

    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd,
            loss='categorical_crossentropy',)
    return model

def train_cbow_base_model():
    min_word_freq = 5
    word_dict = process.get_movie_name_id_dict(min_word_freq=min_word_freq)
    dict_size = len(word_dict)
    emb_size = 100
    context_window_size = 4
    epochs = 20
    batch_size = 128

    model = cbow_base_model(dict_size, emb_size, context_window_size)
    for epoch_id in xrange(epochs):
        # train by batch
        batch_id = 0
        x_batch = []
        y_batch = []
        for movie_ids in process.shuffle(process.reader_creator(word_dict, ngram=context_window_size+1), 10000)():
            batch_id += 1
            if batch_id % (batch_size*50) == 0:
                # Print evaluate log
                score = model.evaluate(np.array(x_batch),
                    keras.utils.to_categorical(y_batch, num_classes=dict_size))
                logger.info('[epoch #%d] batch #%d, train loss:%s' % (epoch_id, batch_id, score))
            if batch_id % batch_size == 0:
                # Convert labels to categorical one-hot encoding
                model.train_on_batch(np.array(x_batch),
                        keras.utils.to_categorical(y_batch, num_classes=dict_size))
                x_batch = []
                y_batch = []
            x = np.array(movie_ids[:context_window_size])
            y = movie_ids[-1]
            x_batch.append(x)
            y_batch.append(y)
    logger.info('model train done')
    # store word embedding
    with open('./models/keras_0804_09_cbow', 'w') as fwrite:
        for idx, vec in enumerate(model.layers[0].get_weights()[0].tolist()):
            fwrite.write('%d %s\n' % (idx, ' '.join([str(_) for _ in vec])))

if __name__ == '__main__':
    # network conf
    paradigm = 'Functional'
    min_word_freq = 10
    word_dict = process.get_movie_name_id_dict(min_word_freq=min_word_freq)
    dict_size = len(word_dict)
    emb_size = 100
    context_window_size = 2
    epochs = 50
    batch_size = 256

    model = skipgram_model(dict_size, emb_size, paradigm)
    #print model.layers
    for epoch_id in xrange(epochs):
        # train by batch
        batch_id = 0
        x_batch = [[],[]]
        y_batch = []
        loss_list = []
        for movie_ids, label in process.shuffle(skipgram_reader_generator(word_dict, context_window=context_window_size), 10000)():
            batch_id += 1
            x_batch[0].append(movie_ids[0])
            x_batch[1].append(movie_ids[1])
            y_batch.append(label)
            if batch_id % (batch_size*1000) == 0:
                # Print evaluate log
                logger.info('[epoch #%d] batch #%d, train loss:%s' % (epoch_id, batch_id, np.mean(loss_list)))
                loss_list = []
            if batch_id % batch_size == 0:
                X = [np.array(x_batch[0]), np.array(x_batch[1])]
                loss = model.train_on_batch(X, np.array(y_batch))
                loss_list.append(loss)
                x_batch = [[],[]]
                y_batch = []
    logger.info('model train done')
    # store word embedding
    with open('./models/keras_0804_09_skipgram', 'w') as fwrite:
        for idx, vec in enumerate(model.layers[2].get_weights()[0].tolist()):
            fwrite.write('%d %s\n' % (idx, ' '.join([str(_) for _ in vec])))
