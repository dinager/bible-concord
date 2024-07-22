import json
import traceback
from typing import Tuple

from server.db_model.db_functions import insert_group_name_to_table, insert_word_to_word_in_group_table
from server.db_model.model.group import GroupModel
from server.db_model.model.word import WordModel
from server.db_model.model.word_in_group import WordInGroupModel


def add_group(group_name: str) -> Tuple[bool, str]:
    try:
        group_name = group_name.lower()
        if GroupModel.does_group_exist(group_name):
            return False, f"group {group_name} already exists"
        insert_group_name_to_table(group_name)
        return True, f"group {group_name} added successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_groups() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        groups = GroupModel.get_all_groups()
        group_names = [group.name for group in groups]

        return True, json.dumps({"groups": group_names})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_words_in_group(group_name: str) -> Tuple[bool, list[str] | str]:
    try:
        group_name = group_name.lower()
        if not GroupModel.does_group_exist(group_name):
            return False, f"group {group_name} doesn't exist"
        words_in_group = WordInGroupModel.get_words_in_group_from_db(group_name)
        return True, words_in_group

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def add_word_to_group(group_name: str, word_value: str) -> Tuple[bool, str]:
    try:
        if not GroupModel.does_group_exist(group_name):
            return False, f"group {group_name} doesn't exist"
        if not WordModel.does_word_exist(word_value):
            return False, f"word {word_value} doesn't exist"
        insert_word_to_word_in_group_table(group_name, word_value)
        return True, f"word {word_value} was added to group {group_name} successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
