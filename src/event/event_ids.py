from enum import Enum, auto

class EvtIds(Enum):
    INVALID_EVT_ID = 0
    ## use to active/deactive the control panel
    EVT_PROJECT_CREATED = auto()
    EVT_PROJECT_LOADED = auto()
    ## use to calculate the shortest distance between 2 grids
    EVT_FIRST_POSITION_SELECTED = auto()
    EVT_SECOND_POSITION_SELECTED = auto()
    EVT_SHORTEST_DISTANCE_CALCULATED = auto()
    EVT_SET_CALC_DISTANCE_MODE = auto()
    ## use to inform display panel operations
    EVT_INFORM_TO_DRAW_GRIDS = auto()
    EVT_INFORM_GET_MAP_DATA = auto()
    EVT_INFORM_SAVE_PROJECT = auto()
    EVT_INFORM_NUMBER_CHANGED = auto()
    EVT_INFORM_LOAD_PICTURE = auto()
    EVT_INFORM_CLEAR_NUMBERS = auto()
    EVT_INFORM_CLEAR_PATH = auto()
    EVT_INFORM_CALC_DISTANCE = auto()
    # use to inform main window
    EVT_GET_PROJECT_NAME = auto()
    EVT_CONTENT_CHANGED = auto()

