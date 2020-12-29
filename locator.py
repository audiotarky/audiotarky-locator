import json
import random
import string
import unittest


RECORD_LENGTH = 4

def generate_record(item, record_length=RECORD_LENGTH):
    '''
    Make a record locator.

    Generates 4 character random string of upper case letters & digits (36
    characters in total) using the item as the seed to the random number
    generator. The same string will generate the same record locator.
    Different strings will most likely make a different record locator. Tested
    below with 10000000 random strings.

    Python uses the Mersenne Twister as the core generator. It produces 53-bit
    precision floats and has a period of 2**19937-1.
    '''
    alphabet = string.ascii_uppercase + string.digits
    random.seed(item)
    return ''.join(random.choices(alphabet, k=record_length))


def find_item(record, lookup={}):
    return lookup[record]


class TestRecordLocator(unittest.TestCase):
    def run_test_strings(self, test_strings, lookup, record_length=4):
        tests = {}
        n_to_test = len(test_strings)
        print(f'Testing {n_to_test} items.')
        # lookup k: v is dummy string: record locator
        reverse_index = {v: k for k, v in lookup.items()}
        for i, t in enumerate(test_strings):
            if i % (n_to_test / 10) == 0:
                print(f'test iter: {1 + int(i / (n_to_test / 10))} : {t}: {lookup[t]}')
            tests[t] = generate_record(t, record_length=record_length)
            # self.assertEqual(lookup[t], tests[t])
            # self.assertEqual(find_item(tests[t], reverse_index), t)
        self.assertCountEqual(tests, lookup, 'duplicate keys locators')
        self.assertCountEqual(tests.values(), list(set(tests.values())), 'duplicate record locators')
        self.assertDictEqual(tests, lookup, msg='dicts do not match')
        print(f'No clash found with {n_to_test} items.')

    def test_expected(self):
        if RECORD_LENGTH != 4:
            raise unittest.SkipTest('Skipping for now')
        expected = {
            'dystopia-is-now/improvisations-1/it-s-getting-dark/1oSNUsqUD-PBRL7awI8AiasWBTEDEwYVo.mp3': 'EVU5',
            'dystopia-is-now/life-is-beautiful-let-s-make-something-short/life-is-beautiful-let-s-make-something-short/1IFRhlX0KWJR6x1CuhV4kCOz75E8MCnGW.wav': 'GMEI',
            'dystopia-is-now/life-is-short-let-s-make-something-beautiful/life-is-beautiful-let-s-make-something-short/1IFRhlX0KWJR6x1CuhV4kCOz75E8MCnGW.wav': 'F1IM',
            'dystopia-is-now/life-is-short-let-s-make-something-beautiful/life-is-short-let-s-make-something-beautiful/1wGf0t864nd4iNtd49Nl2-WFpISDWD3IX.mp3': 'HUTL',
            'dystopia-is-now/notes-from-the-other-place/notes-from-the-other-place/1Jnv02YJjaVZWJL_ghy6nGAefjQnmpXKf.mp3': 'GBGI',
            'https://metsonet.co.uk/music/5pianos.mp3': 'AGQQ',
            'https://metsonet.co.uk/music/absolutely.mp3': '9E32',
            'https://metsonet.co.uk/music/better.mp3': 'DZ2W'
        }
        self.run_test_strings(expected.keys(), expected)
        print(json.dumps(list(expected.values())))

    def generate_data(self, n_to_generate = 1000000, record_length = 4):
        test_data = {}
        for i in range(n_to_generate):
            if i % (n_to_generate / 10) == 0:
                print(f'gen iter: {1 + int(i / (n_to_generate / 10))}')
            dummy = '/'.join(
                [
                    ''.join(random.choices(string.ascii_letters, k=random.randint(4, 24))),
                    ''.join(random.choices(string.ascii_letters, k=random.randint(4, 24))),
                    ''.join(random.choices(string.ascii_letters, k=random.randint(4, 24)))
                ]
            )
            test_data[dummy] = generate_record(dummy, record_length=record_length)
        return test_data

    def test_random(self):
        if RECORD_LENGTH != 4:
            raise unittest.SkipTest('Skipping for now')
        test_data = self.generate_data()
        # k: v is dummy string: record locator
        self.run_test_strings(test_data.keys(), test_data)
        print(test_data.popitem())

    def test_sizes(self):
        failed = False
        msg = ''
        for mult in range(1, 5):
            for l in range(1, 7):
                print(f'Testing record length {l}')
                size = mult * 50 * l
                test_data = self.generate_data(n_to_generate=size, record_length=l)
                # k: v is dummy string: record locator
                try:
                    self.run_test_strings(test_data.keys(), test_data, record_length=l)
                    print(test_data.popitem())
                except AssertionError as ae:
                    msg += f'Failed record length {l} with {size} records. '
                    failed = True
                else:
                    print(f'Passed record length {l} with {size} records')

        self.assertFalse(failed, msg=msg)

if __name__ == "__main__":
    unittest.main()
