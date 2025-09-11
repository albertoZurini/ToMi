import re
from question_recipes import QUESTION_RECIPES
import json


def fix_text(text):
    cleaned = re.sub(r"^\d{1,2}\s*", "", text, flags=re.MULTILINE)
    return "\n".join(cleaned.split("\n")[:-1])


def extract_agent_0(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "enter_agent_0" in trace_parts[i]:
            return story_parts[i].split(" ")[0]


def extract_agent_1(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "enter_agent_1" in trace_parts[i]:
            return story_parts[i].split(" ")[0]


def extract_agent_2(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "enter_agent_2" in trace_parts[i]:
            return story_parts[i].split(" ")[0]


def extract_object(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "object_location" in trace_parts[i]:
            return story_parts[i].split(" ")[1]


def extract_initial_location(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "object_location" in trace_parts[i]:
            return story_parts[i].split(" ")[-1]


def extract_final_location(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "agent_0_moves" in trace_parts[i]:
            return story_parts[i].split(" ")[-1]


def extract_room(story_parts, trace_parts):
    for i in range(len(trace_parts)):
        if "enter_agent_0" in trace_parts[i]:
            return story_parts[i].split(" ")[-1]


def extract_agent_0_exited(story_parts, trace_parts):
    return "agent_0_exits" in trace_parts


def extract_agent_1_exited(story_parts, trace_parts):
    return "agent_1_exits" in trace_parts


def extract_agent_2_exited(story_parts, trace_parts):
    return "agent_2_exits" in trace_parts


def extract_agent_0_exited_before(story_parts, trace_parts):
    if "agent_0_exits" not in trace_parts:
        return False
    else:
        index = trace_parts.index("agent_0_exits")
        if "agent_1_exits" in trace_parts[index:]:
            return True
        else:
            return False


def extract_agent_1_exited_before(story_parts, trace_parts):
    if "agent_1_exits" not in trace_parts:
        return False
    else:
        index = trace_parts.index("agent_1_exits")
        if "agent_0_exits" in trace_parts[index:]:
            return True
        else:
            return False


def extract_state(story, trace):
    story_parts = story.split("\n")
    trace_parts = trace.split(",")

    agent_0 = extract_agent_0(story_parts, trace_parts)
    agent_1 = extract_agent_1(story_parts, trace_parts)
    agent_2 = extract_agent_2(story_parts, trace_parts)
    obj = extract_object(story_parts, trace_parts)
    initial_location = extract_initial_location(story_parts, trace_parts)
    final_location = extract_final_location(story_parts, trace_parts)
    room = extract_room(story_parts, trace_parts)
    is_true_belief = trace_parts[-1] == "true_belief"
    agent_0_exited = extract_agent_0_exited(story_parts, trace_parts)
    agent_1_exited = extract_agent_1_exited(story_parts, trace_parts)
    agent_2_exited = extract_agent_2_exited(story_parts, trace_parts)
    agent_0_exited_before = extract_agent_0_exited_before(story_parts, trace_parts)
    agent_1_exited_before = extract_agent_1_exited_before(story_parts, trace_parts)

    assert agent_0 is not None
    assert agent_1 is not None
    assert obj is not None
    assert initial_location is not None
    assert final_location is not None
    assert room is not None

    agent_0 = agent_0.replace(".", "")
    agent_1 = agent_1.replace(".", "")
    if agent_2 is not None:
        agent_2 = agent_2.replace(".", "")
    obj = obj.replace(".", "")
    initial_location = initial_location.replace(".", "")
    final_location = final_location.replace(".", "")
    room = room.replace(".", "")

    return {
        "agent0": agent_0,
        "agent1": agent_1,
        "agent2": agent_2,
        "object": obj,
        "initial_location": initial_location,
        "final_location": final_location,
        "room": room,
        "is_true_belief": is_true_belief,
        "agent_0_exited": agent_0_exited,
        "agent_1_exited": agent_1_exited,
        "agent_2_exited": agent_2_exited,
        "outside_location": "outside",
        "agent_0_exited_before": agent_0_exited_before,
        "agent_1_exited_before": agent_1_exited_before,
    }


def build_questions(state):
    questions = []
    for recipe in QUESTION_RECIPES:
        question_text = recipe["question_template"].format(**state)
        questions.append(
            {
                "recipe_name": recipe["name"],
                "question": question_text,
                "answer": recipe["get_correct_answer"](state),
            }
        )

    return questions


files = [
    "data/test.txt",
    "data/train.txt",
    "data/val.txt",
]
traces = [
    "data/test.trace",
    "data/train.trace",
    "data/val.trace",
]

all_data = []
all_traces = []

for i in range(len(files)):
    file = files[i]
    trace = traces[i]

    with open(file, "r") as f:
        data = f.read()
    with open(trace, "r") as f:
        trace = f.read()

    data = data.split("1\n")
    trace = trace.split("\n")

    all_data.extend(data)
    all_traces.extend(trace)

all_data = all_data[:100]
all_traces = all_traces[:100]

context_and_questions = []

for i in range(len(all_data)):

    if len(all_data[i]) < 2:
        continue

    entry = {
        "story": fix_text(all_data[i]),
        "trace": all_traces[i],
    }
    pattern = r"^(?=.*agent_1_exits)(?=.*agent_0_moves_obj)(?=.*true_belief).*agent_1_exits(?:(?!agent_1_reenters_loc).)*agent_0_moves_obj.*true_belief.*"

    try:
        re.compile(entry["trace"])
        true_belief = False
    except re.error as e:
        true_belief = True

    if true_belief != "true_belief" in entry["trace"]:
        entry["trace"].replace("true_belief", "false_belief")

    entry["state"] = extract_state(entry["story"], entry["trace"])
    entry["questions"] = build_questions(entry["state"])

    # print(entry["story"])
    # for i in range(0, len(entry["questions"]), 3):
    #     print(entry["questions"][i])

    context_and_questions.append(entry)


def prepare_prompt(text):
    return f"""This is a situation with many characters. At the end, I will ask you to answer a question.
{text}
Think step by step, but then give me a concise reply of one word, enclosed within <answer></answer> tags.
"""


data_to_save = []
i = 0

for el in context_and_questions:
    for q in el["questions"]:
        full_text = el["story"] + "\n" + q["question"]

        data_to_save.append(
            {
                "id": i,
                "recipe_name": q["recipe_name"],
                "is_true_belief": el["state"]["is_true_belief"],
                "prompt": prepare_prompt(full_text),
                "answer": q["answer"],
            }
        )

        i += 1

with open("data/tomi_data.json", "w") as f:
    json.dump(data_to_save, f, indent=2)
