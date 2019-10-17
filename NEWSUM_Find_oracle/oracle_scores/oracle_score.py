import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    
    tags = ['train', 'val', 'test']
    all_scores = dict()


    for tag in tags:

        filename = "oracle_" + tag + ".txt"
        score_data = open(filename, 'r').readlines()
        scores = [float(score.split('\t')[1].strip()) for score in score_data if len(score.strip()) != 0]
        all_scores[tag] = scores

    # sns.set(color_codes =True)

    target_tag = 'val'
    src_file = open("high_score_%s.txt.src" % target_tag , 'w')
    tgt_file = open("high_score_%s.txt.tgt" % target_tag, 'w')
    origin_src = open("../newsum/%s.txt.src" % target_tag, 'r').readlines()
    origin_tgt = open("../newsum/%s.txt.tgt" % target_tag, 'r').readlines()
    num_file = open("high_score_%s_num.txt" % target_tag, 'w')
    threshold = 0.85
    for tag, values in all_scores.items():
        if tag == 'train':
            i = 0
            for v, article, summary in zip(values, origin_src, origin_tgt):
                
                if v > threshold:
                    num_file.write(str(i) + '\n')
                    # src_file.write(article)
                    # tgt_file.write(summary)
                i +=1


        # sns.distplot(values)
        # plt.show()
        print(tag, sum(values)/len(values))

if __name__ == '__main__':
    main()
