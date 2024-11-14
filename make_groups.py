"""
Given a file containing a list of index number - name pairs, 
create groups of a given size or a given number.
"""

import tkinter as tk
from pathlib import Path
from random import randint
from tkinter import filedialog, simpledialog, ttk


class GroupMaker:
    def __init__(self, filepath, *, no_groups=None, group_size=None, seperator=" - "):
        self.seperator    = seperator
        self.filepath     = filepath
        self.no_groups    = no_groups
        self.group_size   = group_size
        self.group_list   = None
        self.groupings    = None
        self.controller()

    def controller(self):
        # check that $no_groups and $group_size were both not supplied
        if (self.no_groups is not None) and (self.group_size is not None):
            raise Exception("$no_groups and $group_size are mutually exclusive!")
        # check that at least $no_groups or $group_size was supplied
        if (self.no_groups is None) and (self.group_size is None):
            raise Exception("Either $no_groups or $group_size must be supplied")
        # validate and parse the content of the file at $filepath
        valid_file, self.group_list = self._validate_file_extract_group_list(
            self.filepath, self.seperator)
        if not valid_file:
            raise Exception("Invalid file supplied!")
        # Create groupings
        # create a certain number of groups
        if self.no_groups:
            self.groupings = self._create_quantity_limited_groups(self.group_list.copy(), self.no_groups)
        # create groups of a certain size
        elif self.group_size:
            self.groupings = self._create_size_limited_groups(self.group_list.copy(), self.group_size)
        self._format_created_groupings(self.groupings)
        ...

    def _validate_file_extract_group_list(self, filepath, seperator) -> (bool, dict):
        """
        Validate the data in the file at $filepath and 
        return a (bool, dict) for the validity of the file content and the valid data.
        dict will be empty if the file is invalid.
        """
        # Check file type and its existance
        if (Path(filepath).suffix != ".txt") or (not Path(filepath).exists()):
            return (False, dict())
        validity = True
        index_name_pairs = dict()
        # get file content
        with open(filepath) as fh:
            file_content = fh.readlines()
        # validate file content
        for line in file_content:
            line = line.strip()
            if not line[:10].isdigit():
                break
            if not line[10:13] == seperator:
                break
            if not len(line[13:]) > 1:
                break
            index_name_pairs[line[:10]] = line[13:]
            ...
        else:
            return (validity, index_name_pairs)
        return (False, dict())

    def _create_quantity_limited_groups(self, group_list, no_groups) -> [tuple, tuple, ...]:
        """
        Using the $group_list, create and return a list containing
        $no_groups groups of unrestricted size.
        """
        group_list = [(key, group_list[key]) for key in group_list]
        groupings = [list() for grp in range(no_groups)]
        current_group_idx = 0
        while group_list:
            random_idx = randint(0, len(group_list)-1)
            random_member = group_list.pop(random_idx)
            if current_group_idx >= no_groups:
                current_group_idx = 0
            groupings[current_group_idx].append(random_member)
            current_group_idx += 1
        return groupings

    def _create_size_limited_groups(self, group_list, group_size) -> [tuple, tuple, ...]:
        """
        Using the $group_list, create and return a list containing
        unrestricted number of $group_size sized groups.
        """
        group_list = [(key, group_list[key]) for key in group_list]
        groupings = list()
        while group_list:
            current_group = list()
            while (len(current_group) < group_size) and (group_list):
                random_idx = randint(0, len(group_list)-1)
                current_group.append(group_list.pop(random_idx))
            groupings.append(current_group)
        return groupings

    def _format_created_groupings(self, groupings, file_format="txt", save_path=None):
        """
        Present the resulting groupings in a $format format.
        """
        output = ""
        match file_format:
            case "txt":
                for idx, group in enumerate(groupings):
                    output += f"GROUP {idx+1}\n"
                    for idx, (index, name) in enumerate(group):
                        output += f"[{idx+1}] {index} - {name}\n"
                    output += "\n"
                print(output)
                if save_path and Path(save_path).exists():
                    with open(save_path, 'w') as fh:
                        fh.write(output)
            case _:
                raise Exception("Only txt supported for now")
        return output




class GUIWrapper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Group Maker")
        self.minsize(500, 500)
        self.resizable(True, True)
        self.input_filepath = None
        self.constraint      = None
        self.controller()

    def controller(self):
        self._create_starter_view(self)
        ...

    def _create_starter_view(self, parent):
        # file selection frame
        file_select_frame = tk.Frame(parent)
        ttk.Label(file_select_frame, text="Select an input file (.txt): ").pack(side="left")
        ttk.Button(file_select_frame, text="select file...", command=self._get_input_filepath).pack(side="left")
        file_select_frame.pack(fill="x", anchor="nw", padx=10, pady=10)
        ...

    def _get_input_filepath(self):
        self.input_filepath = filedialog.askopenfilename()
        print(self.input_filepath)


# GUIWrapper().mainloop()
filepath = r"D:\UserProfilesStorage\Dee\Documents\Coding\Python\group_maker\valid_members_list.txt"
GroupMaker(filepath, group_size=6)