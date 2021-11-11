#!/usr/bin/env python

import csv
import random


def main():
    data = []
    with open('WikiQASent.pos.ans.tsv', 'r', encoding='utf8') as file:
        read_tsv = csv.reader(file, delimiter='\t')
        for line in read_tsv:
            data.append([line[0], line[1], line[5]])

    data.pop(0)
    random.shuffle(data)

    with open('100_question_wikiqa.txt', 'w', encoding='utf8') as file:
        for line in data:
            string = line[0] + "\t" + line[1] + "\t" + line[2] + "\n"
            file.write(string)


if __name__ == '__main__':
    main()