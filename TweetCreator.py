from markovchain import *
from training_algorithms import *

# Builds a formatted string from the generator
def gen(m):
    return ''.join([w for w in m.generate_formatted(word_wrap=200, soft_wrap=True, start_with=None, max_len=25, verbose=True)])

def train_new(obj):
    '''Create new training file from the freshly downloaded texts'''
    
    obj.bulk_train('training_data/*.txt', verbose=True)
    # Store this information for later, so that there's no need to re-train the next time.
    obj.save_training('stored_data/training')
    
    
def load_training(obj):
    '''Loading training information and adjusting weights for a text to be created'''
    
    obj.load_training('stored_data/training')
    
    # Adjust the weights with the help of some fitness functions.
    obj.bulk_adjust_weights(fitness_functions=[aw_favor_rhymes, aw_favor_complexity],
                            iterations=100000,
                            verbose=True)
    
    # Save the new state to a different file, to prevent feedback loops.
    obj.save_training('stored_data/training01')
                            
def initial_training():
    mkv = MarkovChain()
    train_new(mkv)

def create_tweet_text():
    mkv = MarkovChain()

    load_training(mkv)
    tweet = gen(mkv).strip()
    while len(tweet) > 180:
        tweet = gen(mkv).strip()
    
    if tweet[-1] not in ('.', '?', '!'): tweet += '.'
    
    return tweet

