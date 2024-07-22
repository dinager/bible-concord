import json
import traceback
from typing import Tuple

from server.db_model.model.group import GroupModel
from server.db_model.model.word import WordModel
from server.db_model.model.word_in_group import WordInGroupModel


def add_group(group_name: str) -> Tuple[bool, str]:
    try:
        group_name = group_name.lower()
        if GroupModel.does_group_exist(group_name):
            return False, f"group {group_name} already exists"
        GroupModel.insert_group(group_name)
        return True, f"group {group_name} added successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_groups() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        group_names = GroupModel.get_all_groups_names()

        return True, json.dumps({"groups": group_names})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_words_in_group(group_name: str) -> Tuple[bool, list[str] | str]:
    try:
        group_name = group_name.lower()
        if not GroupModel.does_group_exist(group_name):
            return False, f"group {group_name} doesn't exist"
        words_in_group = WordInGroupModel.get_words_in_group(group_name)
        return True, words_in_group

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def add_word_to_group(group_name: str, word_value: str) -> Tuple[bool, str]:
    try:
        group_id = GroupModel.get_group_id(group_name)
        if group_id is None:
            return False, f"group {group_name} doesn't exist"
        word_id = WordModel.get_word_id(word_value)
        if word_id is None:
            return False, f"word {word_value} doesn't exist in any book"
        if WordInGroupModel.does_word_exist_in_group(group_id, word_id):
            return False, f"Group '{group_name}' already has word '{word_value}'"

        WordInGroupModel.insert_word_to_group(group_id, word_id)
        return True, f"word {word_value} was added to group {group_name} successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
