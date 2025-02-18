import textworld
import importlib
import yaml
import json
import os
os.environ['ALFWORLD_DATA'] = '/home/wge/git/alfworld/data'
from typing import Any, List, Dict, Tuple
import sys
from env_history import EnvironmentHistory
from utils import Model, get_chat, get_completion, get_Qwen, get_llama
import textworld.gym

# 设置游戏文件路径
game_path = "./9-cooking-task/game_0_2.ulx"


##############       env_configs

num_envs = 1
env_configs: List[Dict[str, Any]] = []
for i in range(num_envs):
    env_configs += [{
        'name': f'env_{i}',
        'memory': [],
        'is_success': False,
        'skip': False
    }]

####################

#### twworld_run

def alfworld_run(env, base_prompt, memory: List[str], to_print=True, ob='', model: Model = "text-davinci-003") -> Tuple[EnvironmentHistory, bool]:
    if len(memory) > 3:
        env_history = EnvironmentHistory(base_prompt, ob, memory[-3:], [])
    else:
        env_history = EnvironmentHistory(base_prompt, ob, memory, [])
    env_history.reset()
    if to_print:
        print(ob)
        sys.stdout.flush()
    cur_step = 0
    while cur_step < 49:
        action = llm(str(env_history) + ">", stop=['\n'], model=model).strip()
        action = process_action(action)
        env_history.add("action", action)
        # observation, reward, done, info = env.step([action])
        observation, reward, done, info = env.step(action)
        observation = observation.replace('\n\n', '\n')
        # observation, reward, done = process_ob(observation[0]), info['won'][0], done[0]
        if action.startswith('think:'):
            observation = 'OK.'
        env_history.add("observation", observation)
        if to_print:
            print(f'> {action}\n{observation}')
            sys.stdout.flush()
        if done:
            return env_history, True
        # elif env_history.check_is_exhausted():
        #     return env_history, False
        cur_step += 1
    return env_history, False

#################################

### llm

def llm(prompt: str, model: Model, stop: List[str] = ["\n"]):
    try:
        cur_try = 0
        while cur_try < 6:
            if model == "text-davinci-003":
                text = get_completion(prompt=prompt, temperature=cur_try * 0.2, stop_strs=stop)
            elif model == "qwen":
                print("use qwen")
                text = get_Qwen(prompt=prompt, temperature=cur_try * 0.2, stop_strs=stop)
            elif model == "llama":
                print("use llama")
                text = get_llama(prompt=prompt, temperature=cur_try * 0.2, stop_strs=stop)
            else:
                print('no used model')
                return None
                # text = get_chat(prompt=prompt, model=model, temperature=cur_try * 0.2, stop_strs=stop)
            # dumb way to do this
            if len(text.strip()) >= 5:
                return text
            cur_try += 1
        return ""
    except Exception as e:
        print(prompt)
        print(e)
        import sys


def process_ob(ob):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]
    return ob

def process_action(action):
    if action.startswith('>'):
        action = action[1:].strip()
    return action


##########################



world_log_path: str = os.path.join("reflexion_run_logs", 'world.log')
trial_log_path: str = os.path.join("reflexion_run_logs", 'trial.log')
trial_idx = 0

request_infos = textworld.EnvInfos(
    admissible_commands=True,  # All commands relevant to the current state.       # List of all interactable entities found in the game.
)

env_id = textworld.gym.register_game(game_path, request_infos=request_infos)
env = textworld.gym.make(env_id)



num_successes: int = 0
num_additional_successes: int = 0
num_envs: int = len(env_configs)
use_memory = True
model= "qwen"

FOLDER = './prompts'
PROMPT_FILE = 'tw_prompts1.json'
with open(os.path.join(FOLDER, PROMPT_FILE), 'r') as f:
    d = json.load(f)

for z, env_config in enumerate(env_configs):
    ob, info = env.reset()
    ob = '\n'.join(ob.split('\n\n')[2:])
    # name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])

    # print(f"using {name}")

    if env_config["is_success"]:
        num_successes += 1

        # log to world log
        with open(world_log_path, 'a') as wf:
            wf.write(f'Environment #{z} Trial #{trial_idx}: SUCCESS\n')
        with open(trial_log_path, 'a') as wf:
            wf.write(f'\n#####\n\nEnvironment #{z}: Success\n\n#####\n')
        continue

    # for i, (k, v) in enumerate(PREFIXES.items()):
    #     if name.startswith(k):
    # v = 'heat'
    # base_prompt = 'Interact with a household to solve a task. Here are two examples.\n' + d[f'react_{v}_1'] + d[
    #     f'react_{v}_0']
    base_prompt = 'Interact with a household to solve a task. Here is a example.\n' + d['react_easy_0']
    final_env_history, is_success = alfworld_run(env, base_prompt, env_config["memory"] if use_memory else [],
                                                 to_print=True, ob=ob, model=model)

    # update env config
    if is_success:
        status_str: str = f'Environment #{z} Trial #{trial_idx}: SUCCESS'
        env_configs[z]['is_success'] = True
        num_successes += 1
        num_additional_successes += 1
    else:
        status_str: str = f'Environment #{z} Trial #{trial_idx}: FAIL'

    # log to world log
    with open(world_log_path, 'a') as f:
        f.write(status_str + '\n')

    # log env results to trial log
    with open(trial_log_path, 'a') as wf:
        wf.write(
            f'\n#####\n\nEnvironment #{z}:\n{str(final_env_history)}\n\nSTATUS: {"OK" if is_success else "FAIL"}\n\n#####\n')

# close environment object
env.close()