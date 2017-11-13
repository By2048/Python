try:
    from get_summary_md import *
    from get_empty_folder_md import *
    from get_push_bat import *
    from config import *
    from tool import *
except ImportError:
    from .get_summary_md import *
    from .get_empty_folder_md import *
    from .get_push_bat import *
    from .config import *
    from .tool import *


if __name__ == '__main__':

    note_paths = get_all_note_path()

    print('\n------------------------ all node path ------------------------')
    print('\n'.join(note_paths))
    print('------------------------ all node path ------------------------\n')

    for path in note_paths:
        create_empty_folder_md(path)
        create_summary_md(path)

    # create_push_bat()
