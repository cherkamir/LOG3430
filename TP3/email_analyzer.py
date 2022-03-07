import json
import math

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}

    def is_spam(self, subject_orig, body_orig, is_log_prob, is_log_combine, clean_option):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        en fonction du sujet et du texte d'email.
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        # Clean email's subject and body
        email_subject = self.clean_text(subject_orig, clean_option)
        email_body = self.clean_text(body_orig, clean_option)

        # Get the spam/ham probabilities

        # On pose k = 0.6 comme donnée dans l'énoncé pour le coefficient de p_subject.
        k = 0.6
        if is_log_prob:
            log_p_subject_spam, log_p_subject_ham = self.spam_ham_log_subject_prob(
                email_subject)
            log_p_body_spam,    log_p_body_ham = self.spam_ham_log_body_prob(
                email_body)
        else:
            p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(
                email_subject)
            p_body_spam,    p_body_ham = self.spam_ham_body_prob(email_body)

        if is_log_combine:
            if is_log_prob:
                p_sub_spam_text = 0 if log_p_subject_spam == 0 else k * log_p_subject_spam
                p_body_spam_text = 0 if log_p_body_spam == 0 else (
                    1 - k) * log_p_body_spam
                p_spam = math.pow(10, p_sub_spam_text + p_body_spam_text)

                p_sub_ham_text = 0 if log_p_subject_ham == 0 else k * log_p_subject_ham
                p_body_ham_text = 0 if log_p_body_ham == 0 else (
                    1 - k) * log_p_body_ham
                p_ham = math.pow(10, p_sub_ham_text + p_body_ham_text)

            else:
                print(p_subject_spam)
                p_sub_spam_text = 0 if p_subject_spam == 0 else k * \
                    math.log10(p_subject_spam)
                p_body_spam_text = 0 if p_body_spam == 0 else (
                    1 - k) * math.log10(p_body_spam)
                p_spam = math.pow(10, p_sub_spam_text + p_body_spam_text)

                p_sub_ham_text = 0 if p_subject_ham == 0 else k * \
                    math.log10(p_subject_ham)
                p_body_ham_text = 0 if p_body_ham == 0 else (
                    1 - k) * math.log10(p_body_ham)
                p_ham = math.pow(10, p_sub_ham_text + p_body_ham_text)
        else:
            if is_log_prob:
                p_subject_spam = math.pow(10, log_p_subject_spam)
                p_subject_ham = math.pow(10, log_p_subject_ham)
                p_body_spam = math.pow(10, log_p_body_spam)
                p_body_ham = math.pow(10, log_p_body_ham)
            p_spam = k * p_subject_spam + (1 - k) * p_body_spam
            p_ham = k * p_subject_ham + (1 - k) * p_body_ham

        # Compute the merged probabilities

        # Decide is the email is spam or ham
        if p_spam > p_ham:
            return True
        else:
            return False

    def spam_ham_body_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        p_spam = 1.0
        p_ham = 1.0

        voc_data = self.load_dict()

        # Parse the text to compute the probability
        for word in body:
            # Check the spam probability
            if word in voc_data["p_body_spam"]:
                p_spam *= voc_data["p_body_spam"][word]
            else:
                p_spam *= 1.0 / (len(voc_data["p_body_spam"]) + 1.0)

            # Check the ham probability
            if word in voc_data["p_body_ham"]:
                p_ham *= voc_data["p_body_ham"][word]
            else:
                p_ham *= 1.0 / (len(voc_data["p_body_ham"]) + 1.0)

        p_spam *= 0.5925
        p_ham *= 0.4075

        return (p_spam, p_ham)

    def spam_ham_log_body_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        log_p_spam = 0.0
        log_p_ham = 0.0

        voc_data = self.load_dict()

        # Parse the text to compute the probability
        for word in body:
            # Check the spam probability
            if word in voc_data["p_body_spam"]:
                log_p_spam += math.log10(voc_data["p_body_spam"][word])
            else:
                log_p_spam += math.log10(1.0 /
                                         (len(voc_data["p_body_spam"]) + 1.0))

            # Check the ham probability
            if word in voc_data["p_body_ham"]:
                log_p_ham += math.log10(voc_data["p_body_ham"][word])
            else:
                log_p_ham += math.log10(1.0 /
                                        (len(voc_data["p_body_ham"]) + 1.0))

        log_p_spam += math.log10(0.5925)
        log_p_ham += math.log10(0.4075)

        return (log_p_spam, log_p_ham)

    def spam_ham_subject_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        p_spam = 1.0
        p_ham = 1.0

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        for word in subject:
            # Check the spam probability
            if word in voc_data["p_sub_spam"]:
                p_spam *= voc_data["p_sub_spam"][word]
            else:
                p_spam *= 1.0 / (len(voc_data["p_sub_spam"]) + 1.0)

            # Check the ham probability
            if word in voc_data["p_sub_ham"]:
                p_ham *= voc_data["p_sub_ham"][word]
            else:
                p_ham *= 1.0 / (len(voc_data["p_sub_ham"]) + 1.0)

        p_spam *= 0.5925
        p_ham *= 0.4075

        return (p_spam, p_ham)

    def spam_ham_log_subject_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        log_p_spam = 0.0
        log_p_ham = 0.0

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        for word in subject:
            # Check the spam probability
            # Modification with the log formula
            if word in voc_data["p_sub_spam"]:
                log_p_spam += math.log10(voc_data["p_sub_spam"][word])
            else:
                log_p_spam += math.log10(1.0 /
                                         (len(voc_data["p_sub_spam"]) + 1.0))

            # Check the ham probability
            if word in voc_data["p_sub_ham"]:
                log_p_ham += math.log10(voc_data["p_sub_ham"][word])
            else:
                log_p_ham += math.log10(1.0 /
                                        (len(voc_data["p_sub_ham"]) + 1.0))

        log_p_spam += math.log10(0.5925)
        log_p_ham += math.log10(0.4075)

        return (log_p_spam, log_p_ham)

    def clean_text(self, text, clean_option):  # pragma: no cover
        return self.cleaning.clean_text(text, clean_option)

    def load_dict(self):  # pragma: no cover
        # Open vocabulary
        with open(self.vocab) as json_data:
            vocabu = json.load(json_data)

        return vocabu
