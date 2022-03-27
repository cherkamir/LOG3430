from turtle import update
from crud import CRUD
import unittest
from unittest.mock import patch

import datetime

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

    #add_group, update_groups, remove_group, remove_group_member
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_updateGroups_removeGroup_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("2", "Trust", 55)
        crud.remove_group("1")
        crud.remove_group_member("0", "alex@gmail.com")

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])


    #add_group, update_groups, remove_group_member, remove_group
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_updateGroups_removeGroupMember_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("2", "Trust", 55)
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))


    #add_group, remove_group_member, update_groups, remove_group
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_removeGroupMember_updateGroups_removeGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "alex@gmail.com")
        crud.update_groups("2", "Trust", 55)
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))

    
    #add_group, remove_group_member, remove_group, update_groups
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_removeGroupMember_removeGroup_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "alex@gmail.com")
        crud.remove_group("1")
        crud.update_groups("2", "Trust", 55)

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)


    #add_group, remove_group, update_groups, remove_group_member
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_removeGroup_updateGroups_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")
        crud.update_groups("2", "Trust", 55)
        crud.remove_group_member("0", "alex@gmail.com")

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])


    #add_group, remove_group, remove_group_member, update_groups
    @patch("crud.CRUD.read_groups_file") 
    def test_addNewGroup_removeGroup_removeGroupMember_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group("1")
        crud.remove_group_member("0", "alex@gmail.com")
        crud.update_groups("2", "Trust", 55)

        self.assertEqual(crud.get_groups_data("2", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertFalse(crud.get_groups_data("1", "name"))
        self.assertFalse(crud.get_groups_data("1", "Trust"))
        self.assertFalse(crud.get_groups_data("1", "List_of_members"))
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("2", "Trust"), 55)
    

    #remove_group, remove_group_member, add_group, update_groups
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_removeGroupMember_addNewGroup_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.remove_group_member("0", "alex@gmail.com")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("0", "Trust", 55)

        
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)


    #remove_group, remove_group_member, update_groups, add_group
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_removeGroupMember_updateGroups_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.remove_group_member("0", "alex@gmail.com")
        crud.update_groups("0", "Trust", 55)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])


    #remove_group, add_group, remove_group_member, update_groups
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_addNewGroup_removeGroupMember_updateGroups(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "alex@gmail.com")
        crud.update_groups("0", "Trust", 55)

        
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)


    #remove_group, add_group, update_groups, remove_group_member
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_addNewGroup_updateGroups_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.update_groups("0", "Trust", 55)
        crud.remove_group_member("0", "alex@gmail.com")

        
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])


    #remove_group, update_groups, add_group, remove_group_member 
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_updateGroups_addNewGroup_removeGroupMember(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.update_groups("0", "Trust", 55)
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])
        crud.remove_group_member("0", "alex@gmail.com")

        
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])


    #remove_group, update_groups, remove_group_member, add_group
    @patch("crud.CRUD.read_groups_file") 
    def test_removeGroup_updateGroups_removeGroupMember_addNewGroup(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.update_groups("0", "Trust", 55)
        crud.remove_group_member("0", "alex@gmail.com")
        crud.add_new_group("groupeMadum", 90, ["alex@gmail.com", "amir@gmail.com"])

        
        self.assertEqual(crud.get_groups_data("0", "Trust"), 55)
        self.assertEqual(crud.get_groups_data("0", "List_of_members"), ['mark@mail.com'])
        #on a supprime le groupe 1, et en rajoutant groupeMadum, il prend l'id 1.
        self.assertEqual(crud.get_groups_data("1", "List_of_members"), ['alex@gmail.com', 'amir@gmail.com'])



    



