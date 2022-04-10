from crud import CRUD
import unittest
from unittest.mock import patch

class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "1": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "0": {
                "name": "alex@gmail.com",
                "Trust": 70,
                "SpamN": 0,
                "HamN": 50,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "1": {
                "name": "mark@mail.com",
                "Trust": 80,
                "SpamN": 150,
                "HamN": 200,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }


        self.last_deleted_group_infos = {}

        self.groups_data_fields_branches_test = {
            "name": "testField",
            "Trust": 50,
            "List_of_members": ["alex@gmail.com"],
        }

    def tearDown(self):
        pass


    def get_all_groups_data(self, crud):
        '''
        Description: fonction qui retourne tous les groupes y compris tous leurs champs
        Sortie: dictionnaire, contenant les group_datas
        '''
        all_groups_data = {}
        for index in self.groups_data.keys():
            all_groups_data[index] = {}
            for field in ["name", "Trust", "List_of_members"]:
                all_groups_data[str(index)][field] = crud.get_groups_data(index, field)
        return all_groups_data

    def notify_deletion(self, group_id):
        '''
        Description: met à jour le numéro de l'id du dernier groupe à avoir été supprimé
        '''
        self.last_deleted_group_infos["last_deleted_group_id"] = group_id


#----------------------------------------------  TESTS DU CONSTRUCTEUR  ------------------------------------------------#
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_constructeur(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        # On cree l'objet 
        crud = CRUD()
        # Verification que le constructeur initialise bien group_data
        self.assertEqual(self.get_all_groups_data(crud), self.groups_data)

#-----------------------------------------------  TESTS DU RAPPORTEUR  -------------------------------------------------#

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_rapporteur(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on modifie un groupe
        crud.update_groups(1, "name", "Madum")

        expected_new_groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "1": {
                "name": "Madum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


        

#-------------------------------------------  TESTS DES TRANSFORMATEURS  -----------------------------------------------#

############################# 1er transformateur de la séquence : add_group #############################################

    #add_group, update_groups, remove_group, remove_group_member
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_updateGroups_removeGroup_removeGroupMember(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        
        # Verification de l'id si un groupe a ete supprime avant 
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.remove_group_member("2", "alex@gmail.com")

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "2": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members":  ["mark@mail.com"],
            },
        }

        #verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)



        

    #add_group, update_groups, remove_group_member, remove_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_updateGroups_removeGroupMember_removeGroup(self,  mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        crud.remove_group_member("2", "alex@gmail.com")

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "2": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


    #add_group, remove_group_member, update_groups, remove_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_removeGroupMember_updateGroups_removeGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        crud.remove_group_member("0", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(2, field, self.groups_data_fields_branches_test[field])

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        expected_new_groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)




    
    #add_group, remove_group_member, remove_group, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_removeGroupMember_removeGroup_updateGroups(self,  mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        crud.remove_group_member("0", "alex@gmail.com")

        # on supprime le groupe 2
        crud.remove_group(2)
        self.notify_deletion(2)

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(1, field, self.groups_data_fields_branches_test[field])

        expected_new_groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "1": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)



    #add_group, remove_group, update_groups, remove_group_member
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_removeGroup_updateGroups_removeGroupMember(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(2, field, self.groups_data_fields_branches_test[field])

        crud.remove_group_member("0", "alex@gmail.com")


        expected_new_groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)



    #add_group, remove_group, remove_group_member, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_addNewGroup_removeGroup_removeGroupMember_updateGroups(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.remove_group_member("0", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(2, field, self.groups_data_fields_branches_test[field])

        expected_new_groups_data = {
            "0": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"],
            },
            "2": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


############################# 1er transformateur de la séquence : remove_group ##########################################

    #remove_group, remove_group_member, add_group, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_removeGroupMember_addNewGroup_updateGroups(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.remove_group_member("0", "alex@gmail.com")

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group, remove_group_member, update_groups, add_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_removeGroupMember_updateGroups_addNewGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.remove_group_member("0", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


    #remove_group, add_group, remove_group_member, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_addNewGroup_removeGroupMember_updateGroups(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # on supprime alex du groupe 1
        crud.remove_group_member("1", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])


        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


    #remove_group, add_group, update_groups, remove_group_member
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_addNewGroup_updateGroups_removeGroupMember(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        # on supprime alex du groupe 1
        crud.remove_group_member("1", "alex@gmail.com")

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group, update_groups, add_group, remove_group_member
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_updateGroups_addNewGroup_removeGroupMember(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)

        
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))


        # on supprime alex du groupe 1
        crud.remove_group_member("1", "alex@gmail.com")

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group, update_groups, remove_group_member, add_group
     
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroup_updateGroups_removeGroupMember_addNewGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")
        
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))


        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": [],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


############################# 1er transformateur de la séquence : update_groups #########################################

    #update_groups, remove_group, remove_group_member, add_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_removeGroup_removeGroupMember_addNewGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        
        # on supprime alex du groupe 1
        crud.remove_group_member("0", "alex@gmail.com")

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])

        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": [],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members":  ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

#update_groups, remove_group, add_group, remove_group_member
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_removeGroup_addNewGroup_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups("0", "List_of_members", ["amir@gmail.com"])
        crud.remove_group("1")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("1", "alex@gmail.com")

        self.assertEqual(crud.get_groups_data("1", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["amir@gmail.com"])
        self.assertEqual(crud.get_groups_data("0", "name"), "default")

    #update_groups, add_group, remove_group, remove_group_member
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_addNewGroup_removeGroup_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups("0", "Trust", 75)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")
        crud.remove_group_member("2", "alex@gmail.com")

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 75)
        self.assertEqual(crud.get_groups_data("0", "name"), "default")

    #update_groups, add_group, remove_group_member, remove_group
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_addNewGroup_removeGroupMember_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups("0", "Trust", 33)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 33)
        self.assertEqual(crud.get_groups_data("0", "name"), "default")

    #update_groups, remove_group_member, remove_group, add_group
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_removeGroupMember_removeGroup_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups("0", "List_of_members", ["mike@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "amir@gmail.com")
        crud.remove_group("1")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        self.assertEqual(crud.get_groups_data("1", "name"), "groupeMadum")
        self.assertFalse(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mike@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 50)
        self.assertEqual(crud.get_groups_data("0", "name"), "default")

    #update_groups, remove_group_member, add_group, remove_group
    @patch("crud.CRUD.read_groups_file")
    def test_updateGroups_removeGroupMember_addNewGroup_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups("0", "name", "Groupe1")
        crud.remove_group_member("0", "alex@gmail.com")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 50)
        self.assertEqual(crud.get_groups_data("0", "name"), "Groupe1")


############################# 1er transformateur de la séquence : remove_group_member ###################################

    #remove_group_member, update_groups, remove_group, add_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_updateGroups_removeGroup_addNewGroup(self, mock_read_groups_file, mock_read_users_file):

       # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))


        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group_member, update_groups, add_group, remove_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_updateGroups_addNewGroup_removeGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "2": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


    #remove_group_member, add_group, update_groups, remove_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_addNewGroup_updateGroups_removeGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))
            
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])


        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "2": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group_member, add_group, remove_group, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_addNewGroup_removeGroup_updateGroups(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))
            
        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
        
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])


############################# 1er transformateur de la séquence : update_groups #########################################

        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "2": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group_member, remove_group, update_groups, add_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_updateGroups_addNewGroup(self, mock_read_groups_file, mock_read_users_file):

        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
            
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])
        
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))


############################# 1er transformateur de la séquence : remove_group_member ###################################

    #remove_group_member, update_groups, remove_group, add_group
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_updateGroups_removeGroup_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("1", "alex@gmail.com")
        crud.update_groups("0", "List_of_members", ["mike@gmail.com", "amir@gmail.com"])
        crud.remove_group("0")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        self.assertEqual(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), [])
        self.assertFalse(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "name"), "groupeMadum")

    #remove_group_member, update_groups, add_group, remove_group
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_updateGroups_addNewGroup_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("1", "alex@gmail.com")
        crud.update_groups("0", "List_of_members", ["mike@gmail.com", "amir@gmail.com"])
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mike@gmail.com", "amir@gmail.com"])
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")

    #remove_group_member, add_group, update_groups, remove_group
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_addNewGroup_updateGroups_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("0", "alex@gmail.com")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("2", "Trust", 20)
        crud.remove_group("1")

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("2", "Trust"), 20)

    #remove_group_member, add_group, remove_group, update_groups
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_addNewGroup_removeGroup_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("0", "alex@gmail.com")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")
        crud.update_groups("2", "Trust", 20)

        self.assertFalse(crud.get_groups_data("1", "name"), "friends")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("2", "Trust"), 20)

    #remove_group_member, remove_group, update_groups, add_group
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_updateGroups_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")
        crud.update_groups("0", "Trust", 20)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        self.assertEqual(crud.get_groups_data("1", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mark@mail.com"])
        self.assertFalse(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "Trust"), 20)

#remove_group_member, remove_group, update_groups, add_group
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_updateGroups_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")
        crud.update_groups("0", "Trust", 20)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        self.assertEqual(crud.get_groups_data("1", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mark@mail.com"])
        self.assertFalse(crud.get_groups_data("2", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("0", "Trust"), 20)

#remove_group_member, remove_group, add_group, update_groups
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_addNewGroup_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("1", "Trust", 20)

        self.assertEqual(crud.get_groups_data("1", "name"), "groupeMadum")
        self.assertEqual(crud.get_groups_data("1", "Trust"), 20)
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ["mark@mail.com"])
        self.assertFalse(crud.get_groups_data("2", "name"), "groupeMadum")


#-------------------------------------------  TESTS DE LA MÉTHODE AUTRE  -----------------------------------------------#

    @patch("crud.CRUD.read_groups_file")
    def test_autre(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        new_id = crud.get_new_group_id()

        self.assertEqual(new_id, "3")


        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)

    #remove_group_member, remove_group, update_groups, add_group
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_addNewGroup_updateGroups(self, mock_read_groups_file, mock_read_users_file):
        # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
            
        
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))

        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])


        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


#remove_group_member, remove_group, add_group, update_groups
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_removeGroupMember_removeGroup_addNewGroup_updateGroups(self, mock_read_groups_file, mock_read_users_file):
  # mock des fonctions read_groups_file et read_users_file
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()

        # on supprime alex du groupe 0
        crud.remove_group_member("0", "alex@gmail.com")

        # on supprime le groupe 1
        crud.remove_group(1)
        self.notify_deletion(1)
            
        # update_groups avec toutes les branches ou groups_data est modifie
        for field in self.groups_data_fields_branches_test:
            crud.update_groups(0, field, self.groups_data_fields_branches_test[field])
        
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "mark@mail.com"])
        # Verification de l'id si un groupe a ete supprime avant
        group_deleted = 'last_deleted_group_id' in self.last_deleted_group_infos
        if group_deleted:
            last_deleted_group_id = self.last_deleted_group_infos['last_deleted_group_id']
            self.assertEqual(crud.get_group_id("groupeMadum"), str(last_deleted_group_id))



        expected_new_groups_data = {
            "0": {
                "name": "testField",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com"],
            },
            "1": {
                "name": "groupeMadum",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }

        # verification du retour du rapporteur apres les transformations
        self.assertEqual(self.get_all_groups_data(crud), expected_new_groups_data)


#-------------------------------------------  TESTS DE LA MÉTHODE AUTRE  -----------------------------------------------#

    @patch("crud.CRUD.read_groups_file")
    def test_autre(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        new_id = crud.get_new_group_id()

        self.assertEqual(new_id, "3")


