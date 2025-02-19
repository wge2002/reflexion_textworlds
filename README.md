# reflexion_textworlds


# Reflexion Model Deployment for TextWorlds Kitchen Tasks

This repository implements the deployment of the model from the [Reflexion paper](https://arxiv.org/abs/2303.11366) in the TextWorld environment, featuring 32 custom kitchen cooking tasks for testing.

![GitHub](https://img.shields.io/github/license/yourusername/reponame?color=blue)  <!-- Replace with actual badges -->

## Features
- 32 customized kitchen cooking tasks in TextWorld
- Reflexion model integration
- Parallel environment support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/reponame.git
cd reponame
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Execution
```bash
python main.py \
    --num_trials 3 \
    --num_envs 1 \
    --run_name "test_run" \
    --model "4o" \
    --game_path "./32-cooking-task/game_0_1.ulx"
```

### Parameters
| Parameter    | Description                          | Default  |
|--------------|--------------------------------------|----------|
| `--num_trials` | Total number of trials to run        | 3        |
| `--num_envs`   | Number of parallel environments      | 1        |
| `--run_name`    | Identifier for logging/analysis      | "test"   |
| `--model`       | Model version to use                 | "4o"     |
| `--game_path`   | Path to .ulx game file               | Required |

## Custom Tasks
Our 32 kitchen tasks are located in:
```
./32-cooking-task/
└── game_0_1.ulx
    game_0_2.ulx
    ...
    game_31.ulx
```

To use different tasks:
```bash
--game_path "./32-cooking-task/game_X_Y.ulx"  # Replace X,Y with task numbers
```

## Important Notes
⚠️ **Requirements**: Ensure all dependencies are installed before execution  
⚠️ **Resource Warning**: The environment may require significant CPU/RAM resources  
⚠️ **Task Validation**: Verify game file paths before execution

## Contributing
We welcome contributions through:
- 🐛 [Issue Reporting](https://github.com/yourusername/reponame/issues)
- 📥 [Pull Requests](https://github.com/yourusername/reponame/pulls)

Please follow standard GitHub workflows when contributing.

## Citation
If using this implementation, please cite the original Reflexion paper:
```bibtex
@article{shinn2023reflexion,
  title={Reflexion: Language Agents with Verbal Reinforcement Learning},
  author={Shinn, Noah and Labash, Beck and Gopinath, Ashwin},
  journal={arXiv preprint arXiv:2303.11366},
  year={2023}
}

