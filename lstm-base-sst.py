"""
Standard Long Short-Term Memory Network (Zaremba et al. 2014)
    on Stanford Sentiment TreeBank (Socher et al. 2013)

Hyperparameters
- init_scale ... the range of initial weights

Author: Jiho Noh (jiho@cs.uky.edu)
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os
import pandas as pd
import tensorflow as tf


# control flags
flags = tf.flags
flags.DEFINE_string('data_path', 'data/', 'data path contains SST, GloVe')
FLAGS = flags.FLAGS

# global
embedding = None

tf.random_uniform_initializer()


def load_data():
    global embedding

    # read glove
    glove_file = os.path.join(FLAGS.data_path, 'glove/glove.840B.300d.txt')
    try:
        df = pd.read_csv(glove_file, delim_whitespace=True)
        embedding = df.DataFrame.as_Matrix()
    except:
        raise
    print(embedding.shape)

def main(_):
    # pro-process data and load
    load_data()

if __name__ == "__main__":
    tf.app.run()
