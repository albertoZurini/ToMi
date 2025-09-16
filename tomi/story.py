#!/usr/bin/env python3
# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from . import actions
import copy
from enum import Enum
from .world import World
from .oracle import Oracle
from typing import List, Tuple
from . import actions
import numpy as np
from question_recipes import QUESTION_RECIPES


def sample_question(
    oracle_start_state, oracle, agent1, agent2, obj, question, agent_order
):
    idx_dummy = [0]
    if question == "memory":
        action, trace = actions.MemoryAction(oracle_start_state, obj), "memory"
    elif question == "reality":
        action, trace = actions.RealityAction(oracle, obj), "reality"
    elif question == "belief":
        action = actions.BeliefSearchAction(oracle, agent1, agent2, obj)
        trace = f'second_order_{agent_order}_{"" if action.tom else "no_"}tom'
    elif question == "search":
        action = actions.SearchedAction(oracle, agent1, obj)
        trace = f'first_order_{agent_order}_{"" if action.tom else "no_"}tom'
    return action, trace


class StoryType(Enum):
    true_belief = "true_belief"
    false_belief = "false_belief"
    second_order_false_belief = "second_order_false_belief"


def enter(oracle: Oracle, agent: str, observers: List[int], location: str):
    if oracle.get_location(agent) == location:  # already in location
        return actions.LocationAction(oracle, (agent, location))
    else:  # somewhere else, move this person into location
        return actions.EnterAction(oracle, (agent, location), observers)


def generate_story(
    world: World,
) -> Tuple[List[List[actions.Action]], List[List[str]], StoryType]:
    state = {
        "agent0": "agent_0",
        "agent1": "agent_1",
        "agent2": "agent_2",
        "object": "obj",
        "initial_location": "initial_location",
        "final_location": "final_location",
        "room": "room",
        "is_true_belief": False,
        "agent_0_exited": "agent_0_exited",
        "agent_1_exited": "agent_1_exited",
        "agent_2_exited": "agent_2_exited",
        "outside_location": "outside",
        "agent_0_re_entered": False,
        "agent_0_re_entered_same_room": False,
        "agent_1_re_entered": False,
        "agent_1_re_entered_same_room": False,
        "agent_1_thinks_agent_0_is_in": None,
        "agent_0_thinks_agent_1_is_in": None,
        "alt_location": "Diocane",
    }

    oracle = Oracle(world)

    a0, a1, a2 = (world.get_agent() for _ in range(3))
    story_type = StoryType.true_belief

    location = world.get_location()
    state["room"] = location
    alternative_loc = world.get_location()

    # state["alt_location"] = alternative_loc

    # Get an initial object and container in the room
    obj = world.get_object()
    state["object"] = obj
    container_1 = world.get_container()
    container_2 = world.get_container()
    oracle.set_containers(location, [container_1, container_2])
    oracle.set_object_container(obj, container_1)
    state["initial_location"] = container_1
    state["final_location"] = container_2

    trace = []
    chapter = []

    # randomize the order in which agents enter the room
    first_agent = None
    agents = [(a0, 0), (a1, 1)]
    enter_observers = []
    np.random.shuffle(agents)
    agent_0, agent_1 = (x for x, _ in agents)  # TODO: enumerate

    state["agent0"] = a0
    state["agent1"] = a1
    state["agent2"] = a2

    for agent, order in agents:
        chapter.append(enter(oracle, agent, enter_observers, location))
        enter_observers.append(agent)
        trace.append(f"enter_agent_{order}")

    # announce location of object
    chapter.append(actions.ObjectLocAction(oracle, obj, [a for a, _ in agents]))
    trace.append("object_location")
    start_state = copy.deepcopy(oracle)

    # Allow up to 2 location changes and 1 move.  Randomize the order...
    act_types = ["move"] + ["loc_change"] * np.random.randint(1, 3)
    np.random.shuffle(act_types)

    # If we move in the middle, this story moves into the false belief scenario.
    story_type = None

    move_observers = {a0, a1}
    for i, act_type in enumerate(act_types):
        if act_type == "move":
            # move the object to container_2
            chapter.append(
                actions.MoveAction(oracle, (a0, obj, container_2), list(move_observers))
            )
            trace.append(f"agent_0_moves_obj")
        elif oracle.get_location(a1) == location:
            # a2 is in location, exit...
            chapter.append(actions.ExitedAction(oracle, a1))
            move_observers.remove(a1)
            trace.append(f"agent_1_exits")
            state["agent_1_exited"] = True
            ## # Let's see if agent0 is in the room and then update agent0 belief
            ## if "agent_0_exits" in trace:
            ##     # if agent_0 was already exited, their belief doesn't change
            ##     state["agent_0_thinks_agent_1_is_in"] = state["room"]
            ## else:
            ##     state["agent_0_thinks_agent_1_is_in"] = "outside"
            ##     # They can't know which room did agent_1 entered

            # The true/false belief should be set here based on when agent_1 exited
            if "agent_0_moves_obj" in trace:
                story_type = StoryType.true_belief
            else:
                story_type = StoryType.false_belief  # TODO: clean this

        else:
            enter_observers = [a0]
            # Assuming this is the last action, then with 50% chance exit the moving actor
            if np.random.randint(0, 2) == 0 and i == len(act_types) - 1:
                story_type = (
                    StoryType.second_order_false_belief
                )  # this now is a second order false belief
                # We can only do this if this is the last index of act_types, otherwise this agent
                # will try to move the object, but will be in the wrong location
                chapter.append(actions.ExitedAction(oracle, a0))
                move_observers.remove(
                    a0
                )  # EHM..... He's the only one that can move the object, he always sees that, right?
                enter_observers = []
                trace.append(f"agent_0_exits")

                state["agent_0_exited"] = True
                # Let's see if agent1 is in the room and then update agent1 belief
                ## if "agent_1_exits" in trace:
                ##     # if agent_1 was already exited, their belief doesn't change
                ##     state["agent_1_thinks_agent_0_is_in"] = state["room"]
                ## else:
                ##     state["agent_1_thinks_agent_0_is_in"] = "outside"
                ##     # They can't know which room did agent_1 entered

            enter_loc = location if np.random.randint(0, 2) == 0 else alternative_loc
            # a2 already exited, re-enter same room, or a different one
            chapter.append(
                actions.EnterAction(oracle, (a1, enter_loc), enter_observers)
            )
            if enter_loc == location:
                move_observers.add(a1)
                story_type = (
                    StoryType.true_belief
                )  # always true belief is agent_1 re-enters the same room

            trace.append(
                f"agent_1_reenters_" + ("alt_loc" if enter_loc != location else "loc")
            )
            state["agent_1_re_entered"] = True
            state["agent_1_re_entered_same_room"] = enter_loc == location
            state["alt_location"] = enter_loc

            # state["agent_0_"]

    # generate indices for which person 3 should enter/exit
    indices = np.random.choice(
        np.arange(len(chapter) + 1), replace=False, size=np.random.randint(0, 3)
    )
    indices.sort()
    # This is not interesting for us, it's the noise agent
    for idx, action in zip(indices, ["enter", "exit"]):
        if action == "exit":
            chapter.insert(idx, actions.ExitedAction(oracle, a2))
            enter_observers.pop()  # remove person 3 from observers
            trace.insert(idx, f"agent_2_exits")
            state["agent_2_exited"] = True
        else:
            enter_loc = location if np.random.randint(0, 2) == 0 else alternative_loc
            chapter.insert(
                idx, actions.EnterAction(oracle, (a2, enter_loc), enter_observers)
            )
            enter_observers.append(a2)
            trace.insert(idx, f"agent_2_enters")

    # Add noise:
    indices = np.random.choice(
        np.arange(len(chapter) + 1), replace=False, size=np.random.randint(0, 3)
    )
    for idx in indices:
        person = np.random.choice([a0, a1, a2], 1)[0]
        things = world.get_all("objects")
        thing = np.random.choice(things, 1)[0]
        chapter.insert(idx, actions.NoiseAction(oracle, person, thing))
        trace.insert(idx, "noise")

    stories, traces = [], []
    lines_rendered = []
    for line in chapter:
        lines_rendered.append(line.render())
    rendered_story = "\n".join(lines_rendered)

    stories.append(rendered_story)
    traces.append(trace)
    # for q in ["belief"]: # ["memory", "search", "belief", "reality"]:
    #     qtext, qtrace = sample_question(start_state, oracle, a1, a2, obj, q, agent_1)
    #     stories.append(chapter + [qtext])
    #     traces.append(trace + [qtrace])
    # for q in ["search", "belief"]:
    #     qtext, qtrace = sample_question(start_state, oracle, a2, a1, obj, q, agent_2)
    #     stories.append(chapter + [qtext])
    #     traces.append(trace + [qtrace])

    state["is_true_belief"] = story_type == StoryType.true_belief

    agent_0_thinks_agent_1_is_in, agent_1_thinks_agent_0_is_in = get_agents_thought_on_their_locations(state, location, trace)
    state["agent_0_thinks_agent_1_is_in"] = agent_0_thinks_agent_1_is_in
    state["agent_1_thinks_agent_0_is_in"] = agent_1_thinks_agent_0_is_in

    if (
        state["agent_0_thinks_agent_1_is_in"] is None
        or state["agent_1_thinks_agent_0_is_in"] is None
    ):
        pass

    return stories, traces, story_type, state

def get_agents_thought_on_their_locations(state, location, trace):
    agent_0_thinks_agent_1_is_in, agent_1_thinks_agent_0_is_in = None, None

    if state["agent_0_thinks_agent_1_is_in"] is None:
        if "agent_0_exits" not in trace or "agent_0_reenters_loc" in trace:
            # This dude knows all
            if "agent_1_exits" in trace and "agent_1_reenters_loc" not in trace:
                # If agent_1 exited without re-entering
                agent_0_thinks_agent_1_is_in = "outside"
            else:
                agent_0_thinks_agent_1_is_in = location
        else:
            index = trace.index("agent_0_exits")
            interesting_trace = trace[:index]
            if "agent_1_exits" in interesting_trace:
                # This means agent_1 exited before, so agent_0 thinks agent_1 is outside
                agent_0_thinks_agent_1_is_in = "outside"
            else:
                # If agent_1 didn't exit, then
                agent_0_thinks_agent_1_is_in = location

    if state["agent_1_thinks_agent_0_is_in"] is None:
        if "agent_1_exits" not in trace or "agent_1_reenters_loc" in trace:
            # This dude knows all
            if "agent_0_exits" in trace:
                agent_1_thinks_agent_0_is_in = "outside"
            else:
                agent_1_thinks_agent_0_is_in = location

        else:
            index = trace.index("agent_1_exits")
            interesting_trace = trace[:index]
            if "agent_0_exits" in interesting_trace:
                # This means agent_0 exited before, so agent_1 thinks agent_0 is outside
                agent_1_thinks_agent_0_is_in = "outside"
            else:
                # If agent_0 didn't exit, then
                agent_1_thinks_agent_0_is_in = location

    return agent_0_thinks_agent_1_is_in, agent_1_thinks_agent_0_is_in

def test():
    state = {
        "agent0": "agent_0",
        "agent1": "agent_1",
        "agent2": "agent_2",
        "object": "obj",
        "initial_location": "initial_location",
        "final_location": "final_location",
        "room": "room",
        "is_true_belief": False,
        "agent_0_exited": "agent_0_exited",
        "agent_1_exited": "agent_1_exited",
        "agent_2_exited": "agent_2_exited",
        "outside_location": "outside",
        "agent_0_re_entered": False,
        "agent_0_re_entered_same_room": False,
        "agent_1_re_entered": False,
        "agent_1_re_entered_same_room": False,
        "agent_1_thinks_agent_0_is_in": None,
        "agent_0_thinks_agent_1_is_in": None,
        "alt_location": "",
    }
    location = "ciao"
    trace = [
        "enter_agent_1",
        "enter_agent_0",
        "object_location",
        "agent_1_exits",
        "agent_0_moves_obj",
        "agent_0_exits",
        "agent_1_reenters_loc",
    ]
    agent_0_thinks_agent_1_is_in, agent_1_thinks_agent_0_is_in= get_agents_thought_on_their_locations(
        state, location, trace
    )

    print(agent_0_thinks_agent_1_is_in, agent_1_thinks_agent_0_is_in)
