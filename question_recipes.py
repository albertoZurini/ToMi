def logic_get_final_location_o1(state):
    """Returns the immediate, specific final location of OBJECT_1 (e.g., 'table')."""
    return state["final_location_o1"]


def logic_get_primary_room(state):
    """Returns the name of the main room where the action occurs (e.g., 'kitchen')."""
    return state["primary_room"]


def logic_get_outside_location(state):
    """Returns the name of the location outside the main room (e.g., 'garden')."""
    return state["outside_location"]


def logic_get_belief_agent2_location(state):
    """From Agent 1's perspective, Agent 2 entered the room and never left."""
    return state["primary_room"]


def logic_get_belief_agent1_location(state):
    """From Agent 1's perspective, Agent 2 entered the room and never left."""
    return state["outside_location"]


def logic_get_belief_object1_area(state):
    """Agent 1 believes object1 is in the primary room, as it never left."""
    return state["primary_room"]


def logic_get_belief_object1_location(state):
    """
    THIS IS THE CORE FALSE BELIEF TEST.
    If it's a true belief story, Agent 1 saw the move.
    If it's a false belief story, Agent 1 did NOT see the move.
    """
    if state["is_true_belief"]:
        return state["final_location_o1"]  # Bob saw the move, so he knows the new spot.
    else:
        return state[
            "initial_location_o1"
        ]  # Bob left before the move, so he thinks it's in the old spot.


def logic_get_belief_object2_location(state):
    """Agent 1's belief about object2's location is never challenged."""
    return state["outside_location"]


def logic_get_memory_object1_initial_location(state):
    """This is a pure memory check, not a belief about the current state."""
    return state["initial_location_o1"]


def logic_get_memory_object1_final_location(state):
    """This is a pure memory check, not a belief about the current state."""
    return state["final_location_o1"]


def logic_get_perception_of_move(state):
    """This directly checks if Agent 1 witnessed the critical event."""
    return "Yes" if state["is_true_belief"] else "No"


def logic_get_perception_agent1_location_when_object1_moved(state):
    """Where was agent1 when object1 was moved? TB -> inside; FB -> outside"""
    return (
        state["primary_room"] if state["is_true_belief"] else state["outside_location"]
    )


def logic_answer_yes(state):
    return "Yes"


def logic_answer_no(state):
    return "No"


def logic_get_unknown_location(state):
    """This should always return Unknown"""
    return "Unknown"


# --- The List of Recipes ---
QUESTION_RECIPES = [
    # =================================================================================
    # SUBJECT: OBJECT_1 --> Test both IMMEDIATE LOCATION and ENCLOSING AREA
    # =================================================================================
    # --- OBJECT_1 --- IMMEDIATE LOCATION QUERIES ---
    {
        "name": "situation_object1_location_query_set1",
        "question_template": "Pinpoint the final, immediate location of the {object1}.",
        "entities_to_track": ["object1", "final_location_o1", "initial_location_o1"],
        "get_correct_answer": logic_get_final_location_o1,
    },
    {
        "name": "situation_object1_location_query_set2",
        "question_template": "At the end of the story, on what specific surface is the {object1}?",
        "entities_to_track": ["object1", "final_location_o1", "initial_location_o1"],
        "get_correct_answer": logic_get_final_location_o1,
    },
    {
        "name": "situation_object1_location_query_set3",
        "question_template": "After it was moved, what is the exact object the {object1} is on top of?",
        "entities_to_track": ["object1", "final_location_o1", "initial_location_o1"],
        "get_correct_answer": logic_get_final_location_o1,
    },
    # --- OBJECT_1 --- ENCLOSING AREA QUERIES ---
    {
        "name": "situation_object1_area_query_set1",
        "question_template": "At the story's end, which larger room or space contains the {object1}?",
        "entities_to_track": ["object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_object1_area_query_set2",
        "question_template": "In which general area is the {object1} located by the end of the narrative?",
        "entities_to_track": ["object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_object1_area_query_set3",
        "question_template": "When the story finishes, in what kind of room or general space is the {object1} situated?",
        "entities_to_track": ["object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    # =================================================================================
    # SUBJECT: AGENT_1 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_agent1_area_query_set1",
        "question_template": "At the conclusion, in which area is {agent1}?",
        "entities_to_track": ["agent1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    {
        "name": "situation_agent1_area_query_set2",
        "question_template": "Tell me the final general location of {agent1}.",
        "entities_to_track": ["agent1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    {
        "name": "situation_agent1_area_query_set3",
        "question_template": "Where is {agent1} located after all the story's events?",
        "entities_to_track": ["agent1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    # =================================================================================
    # SUBJECT: AGENT_2 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_agent2_area_query_set1",
        "question_template": "At the conclusion, in which area is {agent2}?",
        "entities_to_track": ["agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_agent2_area_query_set2",
        "question_template": "Tell me the final general location of {agent2}.",
        "entities_to_track": ["agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_agent2_area_query_set3",
        "question_template": "Where is {agent2} located after all the story's events?",
        "entities_to_track": ["agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_primary_room,
    },
    # =================================================================================
    # SUBJECT: OBJECT_2 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_object2_area_query_set1",
        "question_template": "Which area holds the {object2} throughout the story?",
        "entities_to_track": ["object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    {
        "name": "situation_object2_area_query_set2",
        "question_template": "In what general location can the {object2} be found?",
        "entities_to_track": ["object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    {
        "name": "situation_object2_area_query_set3",
        "question_template": "What is the enclosing space for the {object2} at the story's end?",
        "entities_to_track": ["object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_outside_location,
    },
    # =================================================================================
    # SUBJECT: INITIAL_LOCATION_O1 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_initial_location_o1_area_query_set1",
        "question_template": "In which area is the {initial_location_o1} contained?",
        "entities_to_track": [
            "primary_room",
            "outside_location",
            "initial_location_o1",
        ],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_initial_location_o1_area_query_set2",
        "question_template": "The {initial_location_o1} is located inside which larger space?",
        "entities_to_track": [
            "primary_room",
            "outside_location",
            "initial_location_o1",
        ],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_initial_location_o1_area_query_set3",
        "question_template": "What is the name of the room that the {initial_location_o1} is in?",
        "entities_to_track": [
            "primary_room",
            "outside_location",
            "initial_location_o1",
        ],
        "get_correct_answer": logic_get_primary_room,
    },
    # =================================================================================
    # SUBJECT: FINAL_LOCATION_O1 --> Test only ENCLOSING AREA
    # =================================================================================
    {
        "name": "situation_final_location_o1_area_query_set1",
        "question_template": "In which area is the {final_location_o1} contained?",
        "entities_to_track": ["primary_room", "outside_location", "final_location_o1"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_final_location_o1_area_query_set2",
        "question_template": "Name the room that contains the {final_location_o1}.",
        "entities_to_track": ["primary_room", "outside_location", "final_location_o1"],
        "get_correct_answer": logic_get_primary_room,
    },
    {
        "name": "situation_final_location_o1_area_query_set3",
        "question_template": "The {final_location_o1} can be found within which general area?",
        "entities_to_track": ["primary_room", "outside_location", "final_location_o1"],
        "get_correct_answer": logic_get_primary_room,
    },
    ##################################################################################################
    # ===============
    # SUBJECT: AGENT1, test agent's belief (what does it think)
    # ========
    #
    # --- Belief about AGENT_2's Location ---
    {
        "name": "belief_agent1_agent2_area_query_set1",
        "question_template": "Where does {agent1} think {agent2} is?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent2_location,
    },
    {
        "name": "belief_agent1_agent2_area_query_set2",
        "question_template": "In {agent1}'s mind, where is {agent2} right now?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent2_location,
    },
    {
        "name": "belief_agent1_agent2_area_query_set3",
        "question_template": "Where does {agent1} think {agent2} is located at the end of the story?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent2_location,
    },
    # --- Belief about AGENT_1's Location ---
    {
        "name": "belief_agent2_agent1_area_query_set1",
        "question_template": "Where does {agent2} think {agent1} is?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_location,
    },
    {
        "name": "belief_agent2_agent1_area_query_set2",
        "question_template": "In {agent2}'s mind, where is {agent1} right now?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_location,
    },
    {
        "name": "belief_agent2_agent1_area_query_set3",
        "question_template": "Where does {agent2} think {agent1} is located at the end of the story?",
        "entities_to_track": ["agent1", "agent2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_agent1_location,
    },
    # --- Belief about Agent1's belief on OBJECT_1's General Area ---
    {
        "name": "belief_agent1_object1_area_query_set1",
        "question_template": "In {agent1}'s view, which larger room contains the {object1}?",
        "entities_to_track": ["agent1", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    {
        "name": "belief_agent1_object1_area_query_set2",
        "question_template": "Which general area does {agent1} believe the {object1} is in?",
        "entities_to_track": ["agent1", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    {
        "name": "belief_agent1_object1_area_query_set3",
        "question_template": "According to {agent1}, what is the overall space where the {object1} is located?",
        "entities_to_track": ["agent1", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    # --- Belief about Agent2's belief on OBJECT_1's General Area ---
    {
        "name": "belief_agent2_object1_area_query_set1",
        "question_template": "In {agent2}'s view, which larger room contains the {object1}?",
        "entities_to_track": ["agent2", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    {
        "name": "belief_agent2_object1_area_query_set2",
        "question_template": "Which general area does {agent2} believe the {object1} is in?",
        "entities_to_track": ["agent2", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    {
        "name": "belief_agent2_object1_area_query_set3",
        "question_template": "According to {agent2}, what is the overall space where the {object1} is located?",
        "entities_to_track": ["agent2", "object1", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object1_area,
    },
    # --- Belief about OBJECT_1's Precise Location (The CRITICAL Test) ---
    {
        "name": "belief_agent1_object1_location_query_set1",
        "question_template": "Where does {agent1} *think* the {object1} is right now?",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_belief_object1_location,
    },
    {
        "name": "belief_agent1_object1_location_query_set2",
        "question_template": "If you asked {agent1} where the {object1} is, what would he say?",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_belief_object1_location,
    },
    {
        "name": "belief_agent1_object1_location_query_set3",
        "question_template": "According to {agent1}'s last observation, on which surface is the {object1}?",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_belief_object1_location,
    },
    # --- Belief about Agent2's belief on OBJECT_1's Precise Location ---
    {
        "name": "belief_agent2_object1_location_query_set1",
        "question_template": "Where does {agent2} *think* the {object1} is right now?",
        "entities_to_track": [
            "agent2",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_final_location,
    },
    {
        "name": "belief_agent2_object1_location_query_set2",
        "question_template": "If you asked {agent2} where the {object1} is, what would he say?",
        "entities_to_track": [
            "agent2",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_final_location,
    },
    {
        "name": "belief_agent2_object1_location_query_set3",
        "question_template": "According to {agent2}'s last observation, on which surface is the {object1}?",
        "entities_to_track": [
            "agent2",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_final_location,
    },
    # --- Belief about Agent1's OBJECT_2's Location ---
    {
        "name": "belief_agent1_object2_area_query_set1",
        "question_template": "Where does {agent1} believe the {object2} is?",
        "entities_to_track": ["agent1", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object2_location,
    },
    {
        "name": "belief_agent1_object2_area_query_set2",
        "question_template": "In {agent1}'s mind, the {object2} is in which area?",
        "entities_to_track": ["agent1", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object2_location,
    },
    {
        "name": "belief_agent1_object2_area_query_set3",
        "question_template": "According to {agent1}'s mental map, in what general location is the {object2}?",
        "entities_to_track": ["agent1", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_belief_object2_location,
    },
    # --- Belief about Agent2's OBJECT_2's Location ---
    {
        "name": "belief_agent2_object2_area_query_set1",
        "question_template": "Where does {agent2} believe the {object2} is?",
        "entities_to_track": ["agent2", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_unknown_location,
    },
    {
        "name": "belief_agent2_object2_area_query_set2",
        "question_template": "In {agent2}'s mind, the {object2} is in which area?",
        "entities_to_track": ["agent2", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_unknown_location,
    },
    {
        "name": "belief_agent2_object2_area_query_set3",
        "question_template": "According to {agent2}'s mental map, in what general location is the {object2}?",
        "entities_to_track": ["agent2", "object2", "primary_room", "outside_location"],
        "get_correct_answer": logic_get_unknown_location,
    },
    ######################
    # --- Perception of the Move Event ---
    {
        "name": "perception_agent1_of_move_query_set1",
        "question_template": "Did {agent1} witness {agent2} moving the {object1}?",
        "entities_to_track": ["agent1", "agent2", "object1"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    {
        "name": "perception_agent1_of_move_query_set2",
        "question_template": "Was {agent1} in the {primary_room} when the {object1} was moved?",
        "entities_to_track": ["agent1", "object1", "primary_room"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    {
        "name": "perception_agent1_of_move_query_set3",
        "question_template": "From {agent1}'s perspective, did he see the {object1} being relocated?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_get_perception_of_move,
    },
    # Can agent1 see object1?
    {
        "name": "perception_agent1_of_object1_query_set1",
        "question_template": "Is {object1} visible to {agent1}?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_object1_query_set2",
        "question_template": "Can {agent1} currently perceive the {object1}?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_object1_query_set3",
        "question_template": "From {agent1}'s point of view, is the {object1} observable?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_answer_no,
    },
    # Can agent1 see object2?
    {
        "name": "perception_agent1_of_object2_query_set1",
        "question_template": "Is {object2} visible to {agent1}?",
        "entities_to_track": ["agent1", "object2"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent1_of_object2_query_set2",
        "question_template": "Can {agent1} currently perceive the {object2}?",
        "entities_to_track": ["agent1", "object2"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent1_of_object2_query_set3",
        "question_template": "From {agent1}'s point of view, is the {object2} observable?",
        "entities_to_track": ["agent1", "object2"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent2 see object1?
    {
        "name": "perception_agent2_of_object1_query_set1",
        "question_template": "Is {object1} visible to {agent2}?",
        "entities_to_track": ["agent2", "object1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_object1_query_set2",
        "question_template": "Can {agent2} currently perceive the {object1}?",
        "entities_to_track": ["agent2", "object1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_object1_query_set3",
        "question_template": "From {agent2}'s point of view, is the {object1} observable?",
        "entities_to_track": ["agent2", "object1"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent2 see object2?
    {
        "name": "perception_agent2_of_object2_query_set1",
        "question_template": "Is {object2} visible to {agent2}?",
        "entities_to_track": ["agent2", "object2"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent2_of_object2_query_set2",
        "question_template": "Can {agent2} currently perceive the {object2}?",
        "entities_to_track": ["agent2", "object2"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent2_of_object2_query_set3",
        "question_template": "From {agent2}'s point of view, is the {object2} observable?",
        "entities_to_track": ["agent2", "object2"],
        "get_correct_answer": logic_answer_no,
    },
    # Can agent1 see initial_location?
    {
        "name": "perception_agent1_of_initial_location_query_set1",
        "question_template": "Can {agent1} see the {initial_location_o1}?",
        "entities_to_track": ["agent1", "initial_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_initial_location_query_set2",
        "question_template": "Is {initial_location_o1} visible to {agent1}?",
        "entities_to_track": ["agent1", "initial_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_initial_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {initial_location_o1} observable?",
        "entities_to_track": ["agent1", "initial_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    # Can agent1 see final location?
    {
        "name": "perception_agent1_of_final_location_query_set1",
        "question_template": "Can {agent1} see the {final_location_o1}?",
        "entities_to_track": ["agent1", "final_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_final_location_query_set2",
        "question_template": "Is {final_location_o1} visible to {agent1}?",
        "entities_to_track": ["agent1", "final_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_final_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {final_location_o1} observable?",
        "entities_to_track": ["agent1", "final_location_o1"],
        "get_correct_answer": logic_answer_no,
    },
    # Can agent2 see initial location?
    {
        "name": "perception_agent2_of_initial_location_query_set1",
        "question_template": "Can {agent2} see the {initial_location_o1}?",
        "entities_to_track": ["agent2", "initial_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_initial_location_query_set2",
        "question_template": "Is {initial_location_o1} visible to {agent2}?",
        "entities_to_track": ["agent2", "initial_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_initial_location_query_set3",
        "question_template": "From {agent2}'s perspective, is the {initial_location_o1} observable?",
        "entities_to_track": ["agent2", "initial_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent2 see final location?
    {
        "name": "perception_agent2_of_final_location_query_set1",
        "question_template": "Can {agent2} see the {final_location_o1}?",
        "entities_to_track": ["agent2", "final_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_final_location_query_set2",
        "question_template": "Is {final_location_o1} visible to {agent2}?",
        "entities_to_track": ["agent2", "final_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_final_location_query_set3",
        "question_template": "From {agent2}'s perspective, is the {final_location_o1} observable?",
        "entities_to_track": ["agent2", "final_location_o1"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent1 see the primary room?
    {
        "name": "perception_agent1_of_primary_room_query_set1",
        "question_template": "Can {agent1} see the {primary_room}?",
        "entities_to_track": ["agent1", "primary_room"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_primary_room_query_set2",
        "question_template": "Is the {primary_room} visible to {agent1}?",
        "entities_to_track": ["agent1", "primary_room"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent1_of_primary_room_query_set3",
        "question_template": "From {agent1}'s perspective, is the {primary_room} observable?",
        "entities_to_track": ["agent1", "primary_room"],
        "get_correct_answer": logic_answer_no,
    },
    # Can agent2 see the primary room?
    {
        "name": "perception_agent2_of_primary_room_query_set1",
        "question_template": "Can {agent2} see the {primary_room}?",
        "entities_to_track": ["agent2", "primary_room"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_primary_room_query_set2",
        "question_template": "Is the {primary_room} visible to {agent2}?",
        "entities_to_track": ["agent2", "primary_room"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent2_of_primary_room_query_set3",
        "question_template": "From {agent2}'s perspective, is the {primary_room} observable?",
        "entities_to_track": ["agent2", "primary_room"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent1 see outside?
    {
        "name": "perception_agent1_of_outside_location_query_set1",
        "question_template": "Can {agent1} see the {outside_location}?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent1_of_outside_location_query_set2",
        "question_template": "Is the {outside_location} visible to {agent1}?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_yes,
    },
    {
        "name": "perception_agent1_of_outside_location_query_set3",
        "question_template": "From {agent1}'s perspective, is the {outside_location} observable?",
        "entities_to_track": ["agent1", "outside_location"],
        "get_correct_answer": logic_answer_yes,
    },
    # Can agent2 see outside?
    {
        "name": "perception_agent2_of_outside_location_query_set1",
        "question_template": "Can {agent2} see the {outside_location}?",
        "entities_to_track": ["agent2", "outside_location"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent2_of_outside_location_query_set2",
        "question_template": "Is the {outside_location} visible to {agent2}?",
        "entities_to_track": ["agent2", "outside_location"],
        "get_correct_answer": logic_answer_no,
    },
    {
        "name": "perception_agent2_of_outside_location_query_set3",
        "question_template": "From {agent2}'s perspective, is the {outside_location} observable?",
        "entities_to_track": ["agent2", "outside_location"],
        "get_correct_answer": logic_answer_no,
    },
    # Where was {agent1} located when the {object1} was moved?\nChoose one of the following areas: {primary_room}, {outside_location}.\nArea:
    {
        "name": "perception_agent1_location_when_object1_moved_area_query_set1",
        "question_template": "Where exactly was {agent1} when the {object1} got relocated?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object1_moved,
    },
    {
        "name": "perception_agent1_location_when_object1_moved_area_query_set2",
        "question_template": "In which place was {agent1} during the movement of the {object1}?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object1_moved,
    },
    {
        "name": "perception_agent1_location_when_object1_moved_area_query_set3",
        "question_template": "What was the location of {agent1} at the time the {object1} was moved?",
        "entities_to_track": ["agent1", "object1"],
        "get_correct_answer": logic_get_perception_agent1_location_when_object1_moved,
    },
]

b = [
    # --- Memory of OBJECT_1's Initial Location ---
    {
        "name": "memory_agent1_object1_initial_location_o1_query_set1",
        "question_template": "Where was the {object1} when {agent1} first entered the room?",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_initial_location,
    },
    {
        "name": "memory_agent1_object1_initial_location_o1_query_set2",
        "question_template": "What was the very first location of the {object1} that {agent1} saw?",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_initial_location,
    },
    {
        "name": "memory_agent1_object1_initial_location_o1_query_set3",
        "question_template": "Pinpoint the original surface the {object1} was on when {agent1} was present.",
        "entities_to_track": [
            "agent1",
            "object1",
            "initial_location_o1",
            "final_location_o1",
        ],
        "get_correct_answer": logic_get_memory_object1_initial_location,
    },
]

# for recipe in QUESTION_RECIPES:
#     original_template = recipe["question_template"]
#     # General template: \nChoices: {rnd_hint_1}/{rnd_hint_2}/{rnd_hint_3}/{rnd_hint_4}\nArea:
#     if "perception" in recipe["name"] and recipe["get_correct_answer"]({"is_true_belief": False, "primary_room": "asf", "outside_location": "asf"}) in ["Yes", "No"]:
#         new_format = "\nChoices: yes, no\nAnswer:"
#     # Check if it's an agent2 belief on the object2 area
#     elif "belief_agent2_object2_area_query" in recipe["name"]:
#         new_format = f"\nChoose one of the following areas: {{primary_room}}, {{outside_location}}, {logic_get_unknown_location(None)}.\nArea:"
#     # Check if it's a 'location' query
#     elif "location_query" in recipe["name"]:
#         new_format = "\nChoose one of the following locations: {initial_location_o1}, {final_location_o1}.\nSpecific Location:"
#     # Check if it's an 'area' query
#     elif "area_query" in recipe["name"]:
#         new_format = "\nChoose one of the following areas: {primary_room}, {outside_location}.\nArea:"
#     recipe["question_template"] = original_template + new_format
