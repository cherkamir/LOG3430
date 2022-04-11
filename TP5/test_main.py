from renege import RENEGE
from vocabulary_creator import VocabularyCreator
import unittest
from main import evaluate


def classify_emails(train_set):
    vocab = VocabularyCreator(train_set)
    vocab.create_vocab()
    renege = RENEGE(train_set)
    renege.classify_emails()


class TestMain(unittest.TestCase):

    def setUp(self):
       self.default_train_set = "train_set.json"
       self.default_test_set = "test_set.json"
       print ("\n--------------------------------------\n")
       print ("Avant le debut de chaque tests avec les fichiers de base ")
       print ("\n--------------------------------------\n")
       classify_emails(self.default_train_set)
       self.default_f1_score = evaluate(self.default_test_set)
       print ("F1 score initial : " + str(self.default_f1_score) )


    def tearDown(self):
        pass
  
    def test_clean_train(self):
        print ("\n--------------------------------------\n")
        print("test clean du train_set.json")
        print ("\n--------------------------------------\n")

        classify_emails("train_clean.json")
        f1_score = evaluate(self.default_test_set)

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)

    def test_clean_test(self):
        print ("\n--------------------------------------\n")
        print("test clean du test_set.json")
        print ("\n--------------------------------------\n")

        f1_score = evaluate("test_clean.json")

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)


    
    def test_permutations_train(self):
        print ("\n--------------------------------------\n")
        print("test 10 permutations de mots du train_set.json")
        print ("\n--------------------------------------\n")

        classify_emails("train_shuffle.json")
        f1_score = evaluate(self.default_test_set)

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)

    def test_permutations_test(self):
        print ("\n--------------------------------------\n")
        print("test 10 permutations de mots du test_set.json")
        print ("\n--------------------------------------\n")

        f1_score = evaluate("test_shuffle.json")

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)


    def test_triple_train(self):
        print ("\n--------------------------------------\n")
        print("test tripler les emails du train_set.json")
        print ("\n--------------------------------------\n")

        classify_emails("train700x3.json")
        f1_score = evaluate(self.default_test_set)

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)

    def test_triple_test(self):
        print ("\n--------------------------------------\n")
        print("test tripler les emails du test_set.json")
        print ("\n--------------------------------------\n")

        f1_score = evaluate("test300x3.json")

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)



    def test_duplicate_train(self):
        print ("\n--------------------------------------\n")
        print("test dupliquer les mots des emails du train_set.json")
        print ("\n--------------------------------------\n")

        classify_emails("train_words.json")
        f1_score = evaluate(self.default_test_set)

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)

    def test_duplicate_test(self):
        print ("\n--------------------------------------\n")
        print("test dupliquer les mots des emails du test_set.json")
        print ("\n--------------------------------------\n")

        f1_score = evaluate("test_words.json")

        print("\nF1 avant la transformation : " + str(self.default_f1_score))
        print("\nF1 apres la transformation : " + str(f1_score))

        self.assertTrue(abs(f1_score - self.default_f1_score) <= 0.03)








        

      

    