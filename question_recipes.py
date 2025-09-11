def logic_get_final_location(state):
    """Returns the immediate, specific final location of OBJECT_1 (e.g., 'table')."""
    return state["final_location"]


def logic_get_room(state):
    """Returns the name of the main room where the action occurs (e.g., 'kitchen')."""
    return state["room"]


def logic_get_outside_location(state):
    """Returns the name of the location outside the main room (e.g., 'garden')."""
    return state["outside_location"]


def logic_get_belief_agent1_think_agent0_is(state):
    if state["agent_1_exited_before"]:
        return state["room"]
    else:
        if state["agent_0_exited"]:
            return state["outside_location"]
        else:
            return state["room"]


def logic_get_belief_agen0_think_agent1_is(state):
    if state["agent_0_exited_before"]:
        return state["room"]
    else:
        if state["agent_1_exited"]:
            return state["outside_location"]
        else:
            return state["room"]


def logic_get_belief_object_area(state):
    """Agent 1 believes object is in the primary room, as it never left."""
    return state["room"]


def logic_get_belief_object_location(state):
    """
    THIS IS THE CORE FALSE BELIEF TEST.
    If it's a true belief story, Agent 1 saw the move.
    If it's a false belief story, Agent 1 did NOT see the move.
    """
    if state["is_true_belief"]:
        return state["final_location"]  # Bob saw the move, so he knows the new spot.
    else:
        return state[
            "initial_location"
        ]  # Bob left before the move, so he thinks it's in the old spot.


def logic_get_memory_object_initial_location(state):
    """This is a pure memory check, not a belief about the current state."""
    return state["initial_location"]


def logic_get_memory_object_final_location(state):
    """This is a pure memory check, not a belief about the current state."""
    return state["final_location"]


def logic_get_perception_of_move(state):
    """This directly checks if Agent 1 witnessed the critical event."""
    return "Yes" if state["is_true_belief"] else "No"


def logic_get_perception_agent1_location_when_object_moved(state):
    """Where was agent1 when object was moved? TB -> inside; FB -> outside"""
    return state["room"] if state["is_true_belief"] else state["outside_location"]


def logic_answer_yes(state):
    return "Yes"


def logic_answer_no(state):
    return "No"


def logic_get_unknown_location(state):
    """This should always return Unknown"""
    return "Unknown"


def logic_answer_object_visible_to_agent1(state):
    return "No" if state["agent_1_exited"] else "Yes"


def logic_answer_object_visible_to_agent0(state):
    return "No" if state["agent_0_exited"] else "Yes"


def logic_answer_initial_location_visible_to_agent1(state):
    return logic_answer_object_visible_to_agent1(state)


def logic_answer_initial_location_visible_to_agent0(state):
    return logic_answer_object_visible_to_agent0(state)


def logic_answer_final_location_visible_to_agent1(state):
    return logic_answer_object_visible_to_agent1(state)


def logic_answer_final_location_visible_to_agent0(state):
    return logic_answer_object_visible_to_agent0(state)


def logic_answer_room_visible_to_agent1(state):
    return logic_answer_object_visible_to_agent1(state)


def logic_answer_room_visible_to_agent0(state):
    return logic_answer_object_visible_to_agent0(state)


def logic_answer_outside_visible_to_agent1(state):
    return "Yes" if state["agent_1_exited"] else "No"


def logic_answer_outside_visible_to_agent0(state):
    return "Yes" if state["agent_0_exited"] else "No"


def logic_get_situation_area_agent1(state):
    return state["outside_location"] if state["agent_1_exited"] else state["room"]


def logic_get_situation_area_agent0(state):
    return state["outside_location"] if state["agent_0_exited"] else state["room"]


# --- The List of Recipes ---
QUESTION_RECIPES = [
    # =================================================================================
    # SUBJECT: OBJECT_1 --> Test both IMMEDIATE LOCATION and ENCLOSING AREA
    # =================================================================================
    # --- OBJECT_1 --- IMMEDIATE LOCATION QUERIES ---
    {
        "name": "situation_object_location_query_set1",
        "question_template": "Pinpoint the final, immediate location of the {object}.",
        "entities_to_track": ["object", "final_location", "initial_location"],
        "get_correct_answer": logic_get_final_location,
    },
    {
        "name": "situation_object_location_query_set2",
        "question_template": "At the end of the story, on what specific surface is the {object}?",
        "entities_to_track": ["object", "final_location", "initial_location"],
        "get_correct_answer": logic_get_final_location,
    },
    {
        "name": "situation_object_location_query_set3",
        "question_template": "After it was moved, what is the exact object the {object} is on top of?",
        "entities_to_track": ["object", "final_location", "initial_location"],
        "get_correct_answer": logic_get_final_location,
    },
    # --- OBJECT_1 --- ENCLOSING AREA QUERIES ---
    {
        "name": "situation_object_area_query_set1",
        "question_template": "At the story's end, which larger room or space contains the {object}?",
        "entities_to_track": ["object", "room", "outside_location"],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_object_area_query_set2",
        "question_template": "In which general area is the {object} located by the end of the narrative?",
        "entities_to_track": ["object", "room", "outside_location"],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_object_area_query_set3",
        "question_template": "When the story finishes, in what kind of room or general space is the {object} situated?",
        "entities_to_track": ["object", "room", "outside_location"],
        "get_correct_answer": logic_get_room,
    },
    # =================================================================================
    # SUBJECT: AGENT_1 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_agent1_area_query_set1",
        "question_template": "At the conclusion, in which area is {agent1}?",
        "entities_to_track": ["agent1", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent1,
    },
    {
        "name": "situation_agent1_area_query_set2",
        "question_template": "Tell me the final general location of {agent1}.",
        "entities_to_track": ["agent1", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent1,
    },
    {
        "name": "situation_agent1_area_query_set3",
        "question_template": "Where is {agent1} located after all the story's events?",
        "entities_to_track": ["agent1", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent1,
    },
    # =================================================================================
    # SUBJECT: AGENT_2 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_agent0_area_query_set1",
        "question_template": "At the conclusion, in which area is {agent0}?",
        "entities_to_track": ["agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent0,
    },
    {
        "name": "situation_agent0_area_query_set2",
        "question_template": "Tell me the final general location of {agent0}.",
        "entities_to_track": ["agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent0,
    },
    {
        "name": "situation_agent0_area_query_set3",
        "question_template": "Where is {agent0} located after all the story's events?",
        "entities_to_track": ["agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_situation_area_agent0,
    },
    # =================================================================================
    # SUBJECT: initial_location --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_initial_location_area_query_set1",
        "question_template": "In which area is the {initial_location} contained?",
        "entities_to_track": [
            "room",
            "outside_location",
            "initial_location",
        ],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_initial_location_area_query_set2",
        "question_template": "The {initial_location} is located inside which larger space?",
        "entities_to_track": [
            "room",
            "outside_location",
            "initial_location",
        ],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_initial_location_area_query_set3",
        "question_template": "What is the name of the room that the {initial_location} is in?",
        "entities_to_track": [
            "room",
            "outside_location",
            "initial_location",
        ],
        "get_correct_answer": logic_get_room,
    },
    # =================================================================================
    # SUBJECT: final_location --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_final_location_area_query_set1",
        "question_template": "In which area is the {final_location} contained?",
        "entities_to_track": ["room", "outside_location", "final_location"],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_final_location_area_query_set2",
        "question_template": "Name the room that contains the {final_location}.",
        "entities_to_track": ["room", "outside_location", "final_location"],
        "get_correct_answer": logic_get_room,
    },
    {
        "name": "situation_final_location_area_query_set3",
        "question_template": "The {final_location} can be found within which general area?",
        "entities_to_track": ["room", "outside_location", "final_location"],
        "get_correct_answer": logic_get_room,
    },
    ##################################################################################################
    # ===============
    # SUBJECT: AGENT1, test agent's belief (what does it think)
    # ========
    #
    # --- Belief about AGENT_2's Location ---
    {
        "name": "belief_agent1_agent0_area_query_set1",
        "question_template": "Where does {agent1} think {agent0} is?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_think_agent0_is,
    },
    {
        "name": "belief_agent1_agent0_area_query_set2",
        "question_template": "In {agent1}'s mind, where is {agent0} right now?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_think_agent0_is,
    },
    {
        "name": "belief_agent1_agent0_area_query_set3",
        "question_template": "Where does {agent1} think {agent0} is located at the end of the story?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_think_agent0_is,
    },
    # --- Belief about AGENT_1's Location ---
    {
        "name": "belief_agent0_agent1_area_query_set1",
        "question_template": "Where does {agent0} think {agent1} is?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agen0_think_agent1_is,
    },
    {
        "name": "belief_agent0_agent1_area_query_set2",
        "question_template": "In {agent0}'s mind, where is {agent1} right now?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agen0_think_agent1_is,
    },
    {
        "name": "belief_agent0_agent1_area_query_set3",
        "question_template": "Where does {agent0} think {agent1} is located at the end of the story?",
        "entities_to_track": ["agent1", "agent0", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_agen0_think_agent1_is,
    },
    # --- Belief about Agent1's belief on OBJECT_1's General Area ---
    {
        "name": "belief_agent1_object_area_query_set1",
        "question_template": "In {agent1}'s view, which larger room contains the {object}?",
        "entities_to_track": ["agent1", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    {
        "name": "belief_agent1_object_area_query_set2",
        "question_template": "Which general area does {agent1} believe the {object} is in?",
        "entities_to_track": ["agent1", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    {
        "name": "belief_agent1_object_area_query_set3",
        "question_template": "According to {agent1}, what is the overall space where the {object} is located?",
        "entities_to_track": ["agent1", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    # --- Belief about agent0's belief on OBJECT_1's General Area ---
    {
        "name": "belief_agent0_object_area_query_set1",
        "question_template": "In {agent0}'s view, which larger room contains the {object}?",
        "entities_to_track": ["agent0", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    {
        "name": "belief_agent0_object_area_query_set2",
        "question_template": "Which general area does {agent0} believe the {object} is in?",
        "entities_to_track": ["agent0", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    {
        "name": "belief_agent0_object_area_query_set3",
        "question_template": "According to {agent0}, what is the overall space where the {object} is located?",
        "entities_to_track": ["agent0", "object", "room", "outside_location"],
        "get_correct_answer": logic_get_belief_object_area,
    },
    # --- Belief about OBJECT_1's Precise Location (The CRITICAL Test) ---
    {
        "name": "belief_agent1_object_location_query_set1",
        "question_template": "Where does {agent1} *think* the {object} is right now?",
        "entities_to_track": [
            "agent1",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_belief_object_location,
    },
    {
        "name": "belief_agent1_object_location_query_set2",
        "question_template": "If you asked {agent1} where the {object} is, what would he say?",
        "entities_to_track": [
            "agent1",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_belief_object_location,
    },
    {
        "name": "belief_agent1_object_location_query_set3",
        "question_template": "According to {agent1}'s last observation, on which surface is the {object}?",
        "entities_to_track": [
            "agent1",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_belief_object_location,
    },
    # --- Belief about agent0's belief on OBJECT_1's Precise Location ---
    {
        "name": "belief_agent0_object_location_query_set1",
        "question_template": "Where does {agent0} *think* the {object} is right now?",
        "entities_to_track": [
            "agent0",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_memory_object_final_location,
    },
    {
        "name": "belief_agent0_object_location_query_set2",
        "question_template": "If you asked {agent0} where the {object} is, what would he say?",
        "entities_to_track": [
            "agent0",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_memory_object_final_location,
    },
    {
        "name": "belief_agent0_object_location_query_set3",
        "question_template": "According to {agent0}'s last observation, on which surface is the {object}?",
        "entities_to_track": [
            "agent0",
            "object",
            "initial_location",
            "final_location",
        ],
        "get_correct_answer": logic_get_memory_object_final_location,
    },
    ######################
    # --- Perception of the Move Event ---
    {
        "name": "perception_agent1_of_move_query_set1",
        "question_template": "Did {agent1} witness {agent0} moving the {object}?",
        "entities_to_track": ["agent1", "agent0", "object"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    {
        "name": "perception_agent1_of_move_query_set2",
        "question_template": "Was {agent1} in the {room} when the {object} was moved?",
        "entities_to_track": ["agent1", "object", "room"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    {
        "name": "perception_agent1_of_move_query_set3",
        "question_template": "From {agent1}'s perspective, did he see the {object} being relocated?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    # Can agent1 see object?
    {
        "name": "perception_agent1_of_object_query_set1",
        "question_template": "Is {object} visible to {agent1}?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_object_query_set2",
        "question_template": "Can {agent1} currently perceive the {object}?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_object_query_set3",
        "question_template": "From {agent1}'s point of view, is the {object} observable?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent1,
    },
    # Can agent0 see object?
    {
        "name": "perception_agent0_of_object_query_set1",
        "question_template": "Is {object} visible to {agent0}?",
        "entities_to_track": ["agent0", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_object_query_set2",
        "question_template": "Can {agent0} currently perceive the {object}?",
        "entities_to_track": ["agent0", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_object_query_set3",
        "question_template": "From {agent0}'s point of view, is the {object} observable?",
        "entities_to_track": ["agent0", "object"],
        "get_correct_answer": logic_answer_object_visible_to_agent0,
    },
    # Can agent1 see initial_location?
    {
        "name": "perception_agent1_of_initial_location_query_set1",
        "question_template": "Can {agent1} see the {initial_location}?",
        "entities_to_track": ["agent1", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_initial_location_query_set2",
        "question_template": "Is {initial_location} visible to {agent1}?",
        "entities_to_track": ["agent1", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_initial_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {initial_location} observable?",
        "entities_to_track": ["agent1", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent1,
    },
    # Can agent1 see final location?
    {
        "name": "perception_agent1_of_final_location_query_set1",
        "question_template": "Can {agent1} see the {final_location}?",
        "entities_to_track": ["agent1", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_final_location_query_set2",
        "question_template": "Is {final_location} visible to {agent1}?",
        "entities_to_track": ["agent1", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_final_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {final_location} observable?",
        "entities_to_track": ["agent1", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent1,
    },
    # Can agent0 see initial location?
    {
        "name": "perception_agent0_of_initial_location_query_set1",
        "question_template": "Can {agent0} see the {initial_location}?",
        "entities_to_track": ["agent0", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_initial_location_query_set2",
        "question_template": "Is {initial_location} visible to {agent0}?",
        "entities_to_track": ["agent0", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_initial_location_query_set3",
        "question_template": "From {agent0}'s perspective, is the {initial_location} observable?",
        "entities_to_track": ["agent0", "initial_location"],
        "get_correct_answer": logic_answer_initial_location_visible_to_agent0,
    },
    # Can agent0 see final location?
    {
        "name": "perception_agent0_of_final_location_query_set1",
        "question_template": "Can {agent0} see the {final_location}?",
        "entities_to_track": ["agent0", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_final_location_query_set2",
        "question_template": "Is {final_location} visible to {agent0}?",
        "entities_to_track": ["agent0", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_final_location_query_set3",
        "question_template": "From {agent0}'s perspective, is the {final_location} observable?",
        "entities_to_track": ["agent0", "final_location"],
        "get_correct_answer": logic_answer_final_location_visible_to_agent0,
    },
    # Can agent1 see the primary room?
    {
        "name": "perception_agent1_of_room_query_set1",
        "question_template": "Can {agent1} see the {room}?",
        "entities_to_track": ["agent1", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_room_query_set2",
        "question_template": "Is the {room} visible to {agent1}?",
        "entities_to_track": ["agent1", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_room_query_set3",
        "question_template": "From {agent1}'s perspective, is the {room} observable?",
        "entities_to_track": ["agent1", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent1,
    },
    # Can agent0 see the primary room?
    {
        "name": "perception_agent0_of_room_query_set1",
        "question_template": "Can {agent0} see the {room}?",
        "entities_to_track": ["agent0", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_room_query_set2",
        "question_template": "Is the {room} visible to {agent0}?",
        "entities_to_track": ["agent0", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_room_query_set3",
        "question_template": "From {agent0}'s perspective, is the {room} observable?",
        "entities_to_track": ["agent0", "room"],
        "get_correct_answer": logic_answer_room_visible_to_agent0,
    },
    # Can agent1 see outside?
    {
        "name": "perception_agent1_of_outside_location_query_set1",
        "question_template": "Can {agent1} see the {outside_location}?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_room_visible_to_agent0,
    },
    {
        "name": "perception_agent1_of_outside_location_query_set2",
        "question_template": "Is the {outside_location} visible to {agent1}?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_outside_visible_to_agent1,
    },
    {
        "name": "perception_agent1_of_outside_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {outside_location} observable?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_outside_visible_to_agent1,
    },
    # Can agent0 see outside?
    {
        "name": "perception_agent0_of_outside_location_query_set1",
        "question_template": "Can {agent0} see the {outside_location}?",
        "entities_to_track": ["agent0", "outside_location"],
        "get_correct_answer": logic_answer_outside_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_outside_location_query_set2",
        "question_template": "Is the {outside_location} visible to {agent0}?",
        "entities_to_track": ["agent0", "outside_location"],
        "get_correct_answer": logic_answer_outside_visible_to_agent0,
    },
    {
        "name": "perception_agent0_of_outside_location_query_set3",
        "question_template": "From {agent0}'s perspective, is the {outside_location} observable?",
        "entities_to_track": ["agent0", "outside_location"],
        "get_correct_answer": logic_answer_outside_visible_to_agent0,
    },
    # Where was {agent1} located when the {object} was moved?\nChoose one of the following areas: {room}, {outside_location}.\nArea:
    {
        "name": "perception_agent1_location_when_object_moved_area_query_set1",
        "question_template": "Where exactly was {agent1} when the {object} got relocated?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object_moved,
    },
    {
        "name": "perception_agent1_location_when_object_moved_area_query_set2",
        "question_template": "In which place was {agent1} during the movement of the {object}?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object_moved,
    },
    {
        "name": "perception_agent1_location_when_object_moved_area_query_set3",
        "question_template": "What was the location of {agent1} at the time the {object} was moved?",
        "entities_to_track": ["agent1", "object"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object_moved,
    },
]

# for recipe in QUESTION_RECIPES:
#     original_template = recipe["question_template"]
#     # General template: \nChoices: {rnd_hint_1}/{rnd_hint_2}/{rnd_hint_3}/{rnd_hint_4}\nArea:
#     if "perception" in recipe["name"] and recipe["get_correct_answer"]({"is_true_belief": False, "room": "asf", "outside_location": "asf"}) in ["Yes", "No"]:
#         new_format = "\nChoices: yes, no\nAnswer:"
#     # Check if it's an agent0 belief on the object2 area
#     elif "belief_agent0_object2_area_query" in recipe["name"]:
#         new_format = f"\nChoose one of the following areas: {{room}}, {{outside_location}}, {logic_get_unknown_location(None)}.\nArea:"
#     # Check if it's a 'location' query
#     elif "location_query" in recipe["name"]:
#         new_format = "\nChoose one of the following locations: {initial_location}, {final_location}.\nSpecific Location:"
#     # Check if it's an 'area' query
#     elif "area_query" in recipe["name"]:
#         new_format = "\nChoose one of the following areas: {room}, {outside_location}.\nArea:"
#     recipe["question_template"] = original_template + new_format
