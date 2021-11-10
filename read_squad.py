#!/usr/bin/env python
import json

def main():
    f = open('squad.json',)
    data = json.load(f)

    for i in data['data']:
        for f in i['paragraphs'][:1]:
            for l in f['qas']:
                answers = []
                for k in l['answers']:
                    if k['text'] not in answers:
                        answers.append(k['text'])
                if answers: 
                    print("{} -- {}".format(l['question'], answers))
     
    # Closing file
    f.close()


if __name__ == '__main__':
    main()