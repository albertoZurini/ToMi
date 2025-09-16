#!/usr/bin/env python3
# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import os
from tomi.story import StoryType, generate_story
from tomi.world import World
from tqdm import tqdm
import numpy as np
import random
from question_recipes import QUESTION_RECIPES
import json


def main(opt):
    N = opt.num_stories
    w = None  # world
    world = World()
    for data_type in ["train"]:  # , "val", "test"]:
        quota = {story_type: N // len(StoryType) for story_type in StoryType}
        stories_path = os.path.join(opt.out_dir, f"{data_type}.txt")
        trace_path = os.path.join(opt.out_dir, f"{data_type}.trace")
        # with open(stories_path, "w") as f, open(trace_path, "w") as trace_f, tqdm(
        #     total=N
        # ) as pbar:
        stories_to_save = []
        for _ in tqdm(range(N)):
            world.reset()
            stories, traces, story_type, state = generate_story(world)

            # if quota[story_type] > 0:
            #     quota[story_type] -= 1
            # else:
            #     # We've already generated enough of this type of story
            #     continue
            for story, trace in zip(stories, traces):
                questions = build_questions(state)

                for q in questions:
                    full_text = story + "\n" + q["question"]

                    stories_to_save.append(
                        {
                            "id": len(stories_to_save),
                            "recipe_name": q["recipe_name"],
                            "is_true_belief": state["is_true_belief"],
                            "prompt": prepare_prompt(full_text),
                            "correct_answer": q["answer"],
                            "trace": trace,
                            "state": state,
                        }
                    )
            #             print(
            #                 "\n".join(
            #                     [f"{i+1} {line.render()}" for i, line in enumerate(story)]
            #                 ),
            #                 file=f,
            #             )
            #             print(",".join(trace + [story_type.value]), file=trace_f)
            #             f.flush()
            # pbar.update(1)

        with open("data/tomi_data.json", "w") as f:
            json.dump(stories_to_save, f, indent=2)


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


def prepare_prompt(text):
    return f"""This is a scenario involving multiple human characters moving between enclosed rooms (e.g., kitchen, bathroom, etc.) and interacting with objects.
* If a character leaves a room and does not re-enter, consider their location to be "outside the current room".
* Rooms are fully enclosed: characters cannot see into other rooms or outside.
* A character can only see what is inside the room they are currently in.
* Track the movements of each character over time. Their memory of objects and events is based only on what they saw while present in a room.
* Also track the location of objects and whether a character can see or interact with them.
* At the end, I will ask a question about what a character knows, sees, or could infer.

{text}
Think step by step, but then provide a concise one-word reply enclosed within <answer></answer> tags."""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", "-s", type=int, default=0, help="Seed for rng")
    parser.add_argument(
        "--num-stories",
        "-n",
        type=int,
        default=100,
        help="Number of stories to generate for each type",
    )
    parser.add_argument("--out-dir", "-o", default="data", help="Output directory")
    opt = parser.parse_args()
    np.random.seed(opt.seed)
    random.seed(opt.seed)

    os.makedirs(opt.out_dir, exist_ok=True)
    main(opt)
