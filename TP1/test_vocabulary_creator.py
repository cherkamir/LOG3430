import json
from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        # données pour mocker "return_value" du "load_dict pour les spam"
        self.mails_spam = {
            "dataset": [
                {
                    "mail": {
                        "Subject": " attention spam spam subject",
                        "From": "GP@paris.com",
                        "Date": "2005-03-04",
                        "Body": "body spam a spam",
                        "Spam": "true",
                        "File": "enronds//enron4/spam/4536.2005-03-04.GP.spam.txt"
                    }
                }
            ]
        }

        self.mails_ham = {
          "dataset": [
                {
                    "mail": {
                        "Subject": " we we nice subject",
                        "From": "GP@paris.com",
                        "Date": "2004-03-09",
                        "Body": "we got nice nice ",
                        "Spam": "false",
                        "File": "enronds//enron4/spam/0559.2004-03-09.GP.spam.txt"
                    }
                }
            ]
        } # données pour mocker "return_value" du "load_dict pour les ham"


        self.clean_subject_spam = ["spam","spam", "subject", "attention"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["body", "spam","spam", "a"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ["we","we","nice","subject"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["we", "got", "nice","nice"]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected_spam = { 
            'p_sub_spam': {'spam': 0.5, 'attention': 0.25, 'subject': 0.25},
            'p_sub_ham': {},
            'p_body_spam': {'body':0.25,'spam':0.5, 'a':0.25},
            'p_body_ham': {}
        }  # vocabulaire avec les valeurs de la probabilité calculées correctement pour les spam

        self.vocab_expected_ham = { 
            'p_sub_spam': {},
            'p_sub_ham': {'we': 0.5, 'nice': 0.25, 'subject': 0.25},
            'p_body_spam': {},
            'p_body_ham': {'we':0.25,'nice':0.5, 'got':0.25}
        }  # vocabulaire avec les valeurs de la probabilité calculées correctement pour les spam

        self.ar_spam = [self.clean_body_spam, self.clean_subject_spam] # array pour les valeurs de retour clean_text de spam avec side_effect
        self.ar_ham = [self.clean_body_ham, self.clean_subject_ham] # array pour les valeurs de retour clean_text de ham avec side_effect
        

    def tearDown(self):
        pass
    def side_effect_spam(self,args):
        # fonction pour implémenter le side_effect pour les spam
        return self.ar_spam.pop()

    def side_effect_ham(self,args):
        # fonction pour implémenter le side_effect pour les ham
        return self.ar_ham.pop()


    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        # Test 
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """

        # on mock la valeur de retour de write_data_to_vocab_file à true
        mock_write_data_to_vocab_file.return_value = True
        # on mock la valeur de retour de load_dict avec des spam qu'on a défini
        mock_load_dict.return_value = self.mails_spam
        # on utilise side_effect pour que la fonction clean_text retourne une valeur différente à chaque appel
        mock_clean_text.side_effect = self.side_effect_spam

        vocab  = VocabularyCreator()

        # on teste si le dictionnaire crée par la fonction est le même que celui qu'on s'attend à avoir
        self.assertEqual(vocab.create_vocab(), self.vocab_expected_spam)
        
        pass
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_ham_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        
        # on mock la valeur de retour de write_data_to_vocab_file à true/   
        mock_write_data_to_vocab_file.return_value = True
        # on mock la valeur de retour de load_dict avec des ham qu'on a défini
        mock_load_dict.return_value = self.mails_ham
        # on utilise side_effect pour que la fonction clean_text retourne une valeur différente à chaque appel
        mock_clean_text.side_effect = self.side_effect_ham

        vocab  = VocabularyCreator()
        # on teste si le dictionnaire crée par la fonction est le même que celui qu'on s'attend à avoir

        self.assertEqual(vocab.create_vocab(), self.vocab_expected_ham)
        
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    def test_write_data_to_vocab_file_successfully_write_vocabulary_with_correct_values(
        self, mock_clean_text, mock_load_dict
    ):

        # Test qui permet de vérifier si les bonnes valeurs sont écrites dans dans le vocabulary.json quand on cree le vocabulaire

        # on mock la valeur de retour de load_dict avec des ham qu'on a défini
        mock_load_dict.return_value = self.mails_ham
        # on utilise side_effect pour que la fonction clean_text retourne une valeur différente à chaque appel
        mock_clean_text.side_effect = self.side_effect_ham
        
        vocab  = VocabularyCreator()

        # On vérifie si la valeur de retour de write_data_to_vocab_file est bien true ( success )
        self.assertEqual(vocab.write_data_to_vocab_file(vocab.create_vocab()),True)

        # on lit les données qui sont dans le fichier .json
        with open("vocabulary.json") as json_data:
            vocab = json.load(json_data)

        # on teste si les donées contenues dans le vocabulary.json sont les mêmes que celles attendues
        self.assertEqual(vocab,self.vocab_expected_ham)
        
        pass



    