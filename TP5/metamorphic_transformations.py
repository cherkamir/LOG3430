import json
import copy
import random
from text_cleaner import TextCleaning


def write_json_file(data, output_file):
    with open(output_file, 'w') as output:
        json.dump(data, output, indent=2)


def clean_emails(source_set, result_file):
    text_cleaner = TextCleaning()
    result = copy.deepcopy(source_set)

    for email in result['dataset']:
        email['mail']['Body'] = ' '.join(text_cleaner.clean_text(email['mail']['Body']))

    write_json_file(result, result_file)


def shuffle_words_order(source_set, result_file):
    result = copy.deepcopy(source_set)

    for email in result['dataset']:
        body = email['mail']['Body'].split(' ')
        for i in range(9):
            index_1 = random.randint(0, len(body) - 1)
            index_2 = random.randint(0, len(body) - 1)

            tmp = body[index_1]
            body[index_1] = body[index_2]
            body[index_2] = tmp

        email['mail']['Body'] = ' '.join(body)

    write_json_file(result, result_file)


def triple_emails(source_set, result_file):
    result = copy.deepcopy(source_set)
    result['dataset'] += source_set['dataset']
    result['dataset'] += source_set['dataset']

    write_json_file(result, result_file)


def duplicate_emails_words(source_set, result_file):
    result = copy.deepcopy(source_set)

    for email in result['dataset']:
        body = email['mail']['Body']
        duplicate_body = body + body
        email['mail']['Body'] = duplicate_body

    write_json_file(result, result_file)


if __name__ == '__main__':
    with open("train_set.json") as email_file:
        train_set = json.load(email_file)

    with open("test_set.json") as test_file:
        test_set = json.load(test_file)

    clean_emails(train_set, "train_clean.json")
    clean_emails(test_set, "test_clean.json")

    shuffle_words_order(train_set, "train_shuffle.json")
    shuffle_words_order(test_set, "test_shuffle.json")

    triple_emails(train_set, "train700x3.json")
    triple_emails(test_set, "test300x3.json")

    duplicate_emails_words(train_set, "train_words.json")
    duplicate_emails_words(test_set, "test_words.json")
