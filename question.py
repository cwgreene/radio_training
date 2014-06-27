#!/usr/bin/env python
import sys
import random
import re
import colorama

class Question(object):
    class BadParse(Exception):
        pass
    def __init__(self, astring):
        result = []
        for line in astring.split("\r\n"):
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
    questions = list(read_questions(open(args[1])))
    try:
        while True:
            question = random.choice(questions)
            print question.question
            guess = raw_input().lower()
            count += 1
            if guess == question.answer.lower():
                print green("Correct!")
                score +=1
            elif guess not in "abcdef":
                break
            else:
                print red("No, "+ question.answer)
    except KeyboardInterrupt:
        pass
    print colorama.Fore.GREEN+"Score:", score, count

main(sys.argv)
