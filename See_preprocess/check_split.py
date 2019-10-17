# -*- coding: utf-8 -*-

import os
import hashlib
from tqdm import tqdm
import re
from nltk.tokenize import word_tokenize

dm_single_close_quote = u'\u2019' # unicode
dm_double_close_quote = u'\u201d'

SENTENCE_START = '<t>'
SENTENCE_END = '</t>'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"] # acceptable ways to end a sentence

url_dir = '../see_preprocessed/cnn-dailymail/'
output_dir = 'cnn_dailymail/entity/'

all_train_urls = url_dir + "url_lists/all_train.txt"
all_val_urls = url_dir + "url_lists/all_val.txt"
all_test_urls = url_dir + "url_lists/all_test.txt"


def read_text_file(text_file):
  lines = []
  with open(text_file, "r") as f:
    for line in f:
      lines.append(line.strip())
  return lines


def hashhex(s):
  """Returns a heximal formated SHA1 hash of the input string."""
  h = hashlib.sha1()
  h.update(s)
  return h.hexdigest()

def get_url_hashes(url_list):
  return [hashhex(url) for url in url_list]

def get_url_hash(url_file):
    url_list = read_text_file(url_file)
    url_hashes = get_url_hashes(url_list)
    return url_hashes

def detect_quote(sentence):

    start_quote = "``"
    end_quote = "''"

    if sentence and start_quote in sentence and end_quote in sentence:
        return True
    else:
        return False

def get_art_abs(story_file):

  lines = read_text_file(story_file)
  
  # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
  lines = [fix_missing_period(line) for line in lines]

  # Separate out article and abstract sentences
  article_lines = []
  highlights = []
  next_is_highlight = False
  for line in lines:
    if line == "":
      continue # empty line
    elif line.startswith("@highlight"):
      next_is_highlight = True
    elif next_is_highlight:
      highlights.append(line)
    else:
      article_lines.append(line)

  # for line in article_lines:
  #   try:
  #     words = word_tokenize(line)
  #   except UnicodeDecodeError:
  #     continue
  #   for i, word in enumerate(words):
  #     try:
  #       word = word.decode('utf-8')
  #     except UnicodeDecodeError:
  #       continue
  #     if word[0].isupper() and i != 0:
  #       if word not in entity:
  #         entity[word] = 1
  #       else:
  #         entity[word] += 1

  #     if word not in word_dict:
  #       word_dict[word] = 1
  #     else:
  #       word_dict[word] += 1

  article = " ".join(article_lines)
  abstract = " ".join([sent for sent in highlights])
  return article, abstract #word_dict, entity
  '''
  article_lines_final = article_lines[:]
  for line in article_lines:
    flag = False
    if not detect_quote(line):
      flag = True # no quote, should delete
      for ch in line[1:]: # Skip first char
        if ch.isupper():
          flag = False # with entity, should keep
          break
    if flag:
      article_lines_final.remove(line)

  # Guarantee at least 3 sentences
  if len(article_lines_final) >=3:
    article_lines = article_lines_final[:]
  '''

  # Lowercase everything
  article_lines = [line.lower() for line in article_lines]
  highlights = [line.lower() for line in highlights]

  # Make article into a single string
  # article = ' '.join(article_lines)
  article = '##SENT##'.join(article_lines)

  # Make abstract into a signle string, putting <s> and </s> tags around the sentences
  # abstract = ' '.join(["%s %s %s" % (SENTENCE_START, sent, SENTENCE_END) for sent in highlights])
  abstract = '##SENT##'.join([sent for sent in highlights])

  return article, abstract

def fix_missing_period(line):
  """Adds a period to a line that is missing a period"""
  if "@highlight" in line: return line
  if line=="": return line
  if line[-1] in END_TOKENS: return line
  # print line[-1]
  return line + " ."

train_hashes = get_url_hash(all_train_urls)
val_hashes = get_url_hash(all_val_urls)
test_hashes = get_url_hash(all_test_urls)

cnn_dir = 'cnn/cnn_stories_tokenized/'
dm_dir = 'dm/dm_stories_tokenized/'

def output_result(hash_list, src_file, tgt_file):

    word_dict = dict()
    entity = dict()

    for hashes in tqdm(hash_list):
        filename =  cnn_dir + hashes + '.story'
        if not os.path.exists(filename):
          filename =  dm_dir + hashes + '.story'
          if not os.path.exists(filename):
            print('QQ')
        # story_file = open(filename, 'r')
        
        # article, abstract = get_art_abs(filename)
        article, abstract = get_art_abs(filename)

        src_file.write(article + '\n')
        tgt_file.write(abstract + '\n')
    
    
    # import json
    
    # key_entity_fp = open(output_dir + "key_entity.json", 'w')
    # json.dump(entity, key_entity_fp)

    # keyword_fp = open(output_dir + "keywords.json", 'w')
    # json.dump(entity, keyword_fp)

    
    # q = 0
    # print("Keyword(entity)")
    # for key, value in sorted(entity.items(), key=lambda x:x[1], reverse=True):
    #   if q < 20:
    #     print(key, value)
    #     q += 1

    # q = 0
    # print("Keyword(all)")
    # for key, value in sorted(word_dict.items(), key=lambda x:x[1], reverse=True):
    #   if q < 20:
    #     print(key, value)
    #     q += 1

# train_src_file = open(output_dir + 'train.txt.src', 'w')
# train_tgt_file = open(output_dir + 'train.txt.tgt', 'w')

# val_src_file = open(output_dir + 'val.txt.src', 'w')
# val_tgt_file = open(output_dir + 'val.txt.tgt', 'w')

output_dir = "/home/jasonsu/文件/grive_backup/Research/bottom-up-summary/bottomup_translate/OpenNMT-py/mask/test/"
test_src_file = open(output_dir + 'test.txt.src', 'w')
test_tgt_file = open(output_dir + 'test.txt.tgt', 'w')

# output_result(train_hashes, train_src_file, train_tgt_file)
# output_result(val_hashes, val_src_file, val_tgt_file)
output_result(test_hashes, test_src_file, test_tgt_file)

