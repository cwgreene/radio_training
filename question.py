#!/usr/bin/env python
import sys
import random
import re
import colorama
import argparse

class Question(object):
    class BadParse(Exception):
        pass
    def __init__(self, astring):
        result = []
        for line in astring.split("\n"):
            if re.match("^T[0-9][A-Z][0-9]*", line):
                self.header = line
                self.answer = re.findall(r"T[0-9][A-Z][0-9]* \(([A-Z])\)", line)[0]
            else:
                result += [line]
        self.question = "\n".join(result)
        if not hasattr(self, "answer"):
            raise Question.BadParse(astring)

def read_questions(afile):
    current_question = ""
    for line in afile:
        if line.startswith("~~"):
            yield Question(current_question)
            current_question = ""
        elif line.startswith("~@"):
            current_question = ""
        elif line.startswith("~#"):
            current_question = ""
        else:
            current_question += line

def green(astring):
    return colorama.Fore.GREEN + astring + colorama.Fore.RESET

def red(astring):
    return colorama.Fore.RED + astring + colorama.Fore.RESET

def main(args):
    score = 0
    count = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("questionfile", help="File containing questions")
    options = parser.parse_args(args)

    print(options.questionfile)
    with open(options.questionfile) as qf:
        questions = list(read_questions(qf))

    try:
        while True:
            question = random.choice(questions)
            print(question.question)
            guess = input().lower()
            count += 1
            if guess == question.answer.lower():
                print(green("Correct!"))
                score +=1
            elif guess not in "abcdef":
                break
            else:
                print(red("No, "+ question.answer))
    except KeyboardInterrupt:
        pass
    print(colorama.Fore.GREEN+"Score:", score, count, colorama.Fore.RESET)
main(sys.argv[1:])
