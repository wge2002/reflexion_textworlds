import os
import json
import argparse

from textworld_trial import run_trial
from generate_reflections import update_memory

from typing import Any, List, Dict

from langchain_openai import ChatOpenAI
import subprocess
import os
import os
import subprocess
import requests
from dotenv import load_dotenv

def set_proxy_via_python(proxy_ip, port=10808):
    proxy_http = f"http://{proxy_ip}:{port}"
    
    # 设置环境变量
    os.environ['HTTP_PROXY'] = proxy_http
    os.environ['HTTPS_PROXY'] = proxy_http
    os.environ['ALL_PROXY'] = proxy_http
    
    # 配置 Git 代理
    try:
        subprocess.run(['git', 'config', '--global', 'http.proxy', proxy_http], check=True)
        subprocess.run(['git', 'config', '--global', 'https.proxy', proxy_http], check=True)
        print("代理环境变量和 Git 配置已设置。")
    except subprocess.CalledProcessError as e:
        print("配置 Git 代理失败:", e)

def unset_proxy_via_python():
    # 取消环境变量
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    os.environ.pop('ALL_PROXY', None)
    
    # 取消 Git 代理配置
    try:
        subprocess.run(['git', 'config', '--global', '--unset', 'http.proxy'], check=True)
        subprocess.run(['git', 'config', '--global', '--unset', 'https.proxy'], check=True)
        print("代理环境变量和 Git 配置已取消。")
    except subprocess.CalledProcessError as e:
        print("取消 Git 代理配置失败:", e)

def get_default_gateway_ip():
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True, check=True)
        default_route = next(line for line in result.stdout.splitlines() if 'default' in line)
        winip = default_route.split()[2]
        return winip
    except (subprocess.CalledProcessError, StopIteration, IndexError) as e:
        print("无法获取默认网关 IP:", e)
        return None
    
winip = get_default_gateway_ip()
if winip:
    set_proxy_via_python(winip, port=10808)  

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_trials", type=int, default=1, help="The number of trials to run")
    parser.add_argument("--num_envs", type=int, default=1, help="The number of environments per trial")
    parser.add_argument("--run_name", type=str, default="reflexion_run", help="The name of the run")
    parser.add_argument("--use_memory", default= True, action='store_true', help="Allow the Agent to use memory")
    parser.add_argument("--is_resume", default= False, action='store_true',  help="To resume run")
    parser.add_argument("--resume_dir", type=str, default="", help="If resume, the logging directory")
    parser.add_argument("--start_trial_num", type=int, default=0, help="If resume, the start trial num")
    parser.add_argument("--model", type=str, default="qwen", help="The model to use. One of `gpt-4`, `gpt-3.5-turbo`, or `text-davinci-003")
    parser.add_argument("--game_path", type=str, default="", help="the path to the textworld game")
    args = parser.parse_args()

    assert args.num_trials > 0, "Number of trials should be positive"
    assert args.num_envs > 0, "Number of environments should be positive"

    return args

def main(args) -> None:
    if args.is_resume:
        if not os.path.exists(args.resume_dir):
            raise ValueError(f"Resume directory `{args.resume_dir}` does not exist")
        logging_dir = args.resume_dir

        # load environment configs
        env_config_path: str = os.path.join(args.resume_dir, f'env_results_trial_{args.start_trial_num - 1}.json')
        if not os.path.exists(env_config_path):
            raise ValueError(f"Environment config file `{env_config_path}` does not exist")
        with open(env_config_path, 'r') as rf:
            env_configs: List[Dict[str, Any]] = json.load(rf)
    else:
        # Create the run directory
        if not os.path.exists(args.run_name):
            os.makedirs(args.run_name)
        logging_dir = args.run_name

        # initialize environment configs
        env_configs: List[Dict[str, Any]] = []
        for i in range(args.num_envs):
            env_configs += [{
                'name': f'env_{i}',
                'memory': [],
                'is_success': False,
                'skip': False
            }]
    
    world_log_path: str = os.path.join(logging_dir, 'world.log')

    # print start status to user
    if args.is_resume:
        print(f"""
    -----
    Resuming run with the following parameters:
    Run name: {logging_dir}
    Number of trials: {args.num_trials}
    Number of environments: {args.num_envs}
    Use memory: {args.use_memory}
    Resume trial number: {args.start_trial_num}

    Sending all logs to `{args.run_name}`
    -----
    """)
    else:
        print(f"""
    -----
    Starting run with the following parameters:
    Run name: {logging_dir}
    Number of trials: {args.num_trials}
    Number of environments: {args.num_envs}
    Use memory: {args.use_memory}

    Sending all logs to `{args.run_name}`
    -----
    """)

    # run trials
    trial_idx = args.start_trial_num
    while trial_idx < args.num_trials:
        with open(world_log_path, 'a') as wf:
            wf.write(f'\n\n***** Start Trial #{trial_idx} *****\n\n')

        # set paths to log files
        trial_log_path: str = os.path.join(args.run_name, f'trial_{trial_idx}.log')
        trial_env_configs_log_path: str = os.path.join(args.run_name, f'env_results_trial_{trial_idx}.json')
        if os.path.exists(trial_log_path):
            open(trial_log_path, 'w').close()
        if os.path.exists(trial_env_configs_log_path):
            open(trial_env_configs_log_path, 'w').close()

        # run trial
        run_trial(trial_log_path, world_log_path, trial_idx, env_configs, args.use_memory, args.model, args.game_path)

        # update memory if needed
        if args.use_memory:
            env_configs: List[Dict[str, Any]] = update_memory(trial_log_path, env_configs)

        # log env configs for trial
        with open(trial_env_configs_log_path, 'w') as wf:
            json.dump(env_configs, wf, indent=4)

        # log world for trial
        with open(world_log_path, 'a') as wf:
            wf.write(f'\n\n***** End Trial #{trial_idx} *****\n\n')

        trial_idx += 1


if __name__ == '__main__':
    args = get_args()
    main(args)
