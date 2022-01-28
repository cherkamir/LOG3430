from turtle import update
from crud import CRUD
import unittest
from unittest.mock import patch

import datetime

class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass



    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file" pour tester que l'information a ajouter pour l'utilisateur a été formée correctement
        par la fonction, e.g. self.modify_users_file(data) -> "data" doit avoir un format et contenu expecté
        il faut utiliser ".assert_called_once_with(expected_data)"

        Note: Ce test a deja ete complete pour vous
        """

        # Ici on mock pour que read_users_file retourne la liste d'utilisateurs
        mock_read_users_file.return_value = self.users_data

        # Les informations du nouvel utilisateur
        new_user_data = {
                "name": "james@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }

        # On effectue une copie de la liste d'utilisateurs
        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        # On ajoute les infos du nouvel utilisateur
        users_data_final["0"] = new_user_data

        crud = CRUD()
        crud.add_new_user("james@gmail.com", "2020-08-08")
        # On vérifie que quand on ajoute un nouvel utilisateur, modify_users_file est appelée avec la nouvelle liste mise à jour
        mock_modify_users_file.assert_called_once_with(users_data_final)
          		

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")    
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a été formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_user("amir@gmail.com", "2020-08-08")
        crud.add_new_user("mike@gmail.com", "2020-08-12")
        crud.add_new_user("test@gmail.com", "2020-08-15")

        # Les informations du nouveau groupe
        new_group_data = {
            "name": "groupTest",
            "Trust": 90,
            "List_of_members": ["amir@gmail.com", "mike@gmail.com", "test@gmail.com"],
        }

        groups_data_final = {}
        groups_data_final["1"] = self.groups_data["1"]
        groups_data_final["2"] = self.groups_data["2"]
        groups_data_final["0"] = new_group_data

        
        crud.add_new_group("groupTest", 90, ["amir@gmail.com", "mike@gmail.com", "test@gmail.com"])

        # On vérifie que quand on ajoute un nouveau groupe, modify_groups_file est appelée avec la nouvelle liste mise à jour
        mock_modify_groups_file.assert_called_once_with(groups_data_final)


        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_users_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si ID non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data("3", "SpamN"))

        pass
        

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si champ non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data("1", "whatever"))
        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ et id valide sont utilises
        il faut utiliser ".assertEqual()""
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data("1", "Trust"), 100)

        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_id mais pour un groupe
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_groups_data("3", "Trust"))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_field mais pour un groupe
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_groups_data("1", "whatever"))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_correct_value_if_field_and_id_are_valid mais pour un groupe
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.get_groups_data("1", "Trust"), 50)
        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):

        mock_read_users_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_groups_data("1", "Trust"), 25)

        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("alex@gmail.com"), "1")
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_id("whatever"))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.get_group_id("default"), "1")
        
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    # Modify_user_file mock est inutile pour tester False pour update
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users("3", "Trust", 33))

        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users("1", "whatever", 33))

        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """

        mock_read_users_file.return_value = self.users_data

        updated_user_data = {
                "name": "alex@gmail.com",
                "Trust": 33,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }    

        users_data_final = {}
        users_data_final["1"] = updated_user_data
        users_data_final["2"] = self.users_data["2"]

        crud = CRUD()
        crud.update_users("1", "Trust", 33)
        mock_modify_users_file.assert_called_once_with(users_data_final)
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups("3", "Trust", 33))
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups("1", "whatever", 33))

        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """

        mock_read_groups_file.return_value = self.groups_data

        updated_group_data = {
                "name": "default",
                "Trust": 33,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            }

        groups_data_final = {}
        groups_data_final["1"] = updated_group_data
        groups_data_final["2"] = self.groups_data["2"]

        crud = CRUD()
        crud.update_groups("1", "Trust", 33)
        mock_modify_groups_file.assert_called_once_with(groups_data_final)
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user("3"))
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data 

        users_data_final = {}
        users_data_final["2"] = self.users_data["2"]

        crud = CRUD()
        crud.remove_user(1)
        mock_modify_users_file.assert_called_once_with(users_data_final)
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user_group("3", "default"))
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user_group("1", "whatever"))
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data


        updated_users_data = {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": [],
            }

        updated_users_final = {}
        updated_users_final["1"] = updated_users_data
        updated_users_final["2"] = self.users_data["2"]


        crud = CRUD()
        crud.remove_user_group("1", "default")
        mock_modify_users_file.assert_called_once_with(updated_users_final )

        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.remove_group("3"))


        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        removed_group = {
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        remove_group_final = {}
        remove_group_final["2"] = removed_group["2"]

        crud = CRUD()
        crud.remove_group("1")

        mock_modify_groups_file.assert_called_once_with(remove_group_final)
        

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()

        self.assertFalse(crud.remove_group_member("3", "alex@gmail.com"))
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()

        self.assertFalse(crud.remove_group_member("1", "whatever@gmail.com"))
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        
        removed_group_member = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
        }

        removed_member_final = {}
        removed_member_final["1"] = removed_group_member["1"]
        removed_member_final["2"] = self.groups_data["2"]

        crud = CRUD()
        crud.remove_group_member("1", "alex@gmail.com")
        mock_modify_groups_file.assert_called_once_with(removed_member_final)
        pass
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    # @patch("crud.CRUD.get_new_user_id")
    @patch("crud.CRUD.read_users_file")
    def test_get_new_user_id_returns_the_correct_id(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        # print(crud.get_new_user_id())
        self.assertEqual(crud.get_new_user_id(), "0")

