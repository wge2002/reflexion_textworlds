# reflexion_textworlds

Introduction
This repository mainly implements the deployment of the model from the Reflexion paper in the TextWorlds environment. We have custom - set 32 kitchen cooking tasks for testing and running the model in the TextWorlds environment.
Installation of Dependencies
Before running this project, make sure you have installed all the required dependencies. You can install all the dependencies listed in the requirements.txt file by running the following command:
bash
pip install -r requirements.txt
Running Steps
After installing the dependencies, you can start the project by executing the main.py script. Here is a running example, and you can adjust the parameters according to your needs:
bash
python main.py \
        --num_trials 3 \
        --num_envs 1 \
        --run_name "test" \
        --model "4o" \
        --game_path "./32-cooking-task/game_0_1.ulx"
Parameter Explanation
--num_trials: Number of trials, specifying the total number of trials the model will conduct.
--num_envs: Number of environments, indicating the number of simultaneously running environment instances.
--run_name: Run name, used to identify this run for subsequent recording and analysis.
--model: Model name, specifying the model to be used.
--game_path: Game file path, pointing to a specific game file among the custom 32 kitchen cooking tasks.
Custom Tasks
The 32 kitchen cooking tasks in this project are all set by ourselves. These tasks are stored in the 32 - cooking - task directory, and each task corresponds to a .ulx file. You can choose different task files for testing as needed.
Notes
Please ensure that all the dependencies have been correctly installed before running the project; otherwise, the program may run incorrectly.
The running process may consume a certain amount of system resources. Please make sure your computer has sufficient performance.
Contribution and Feedback
If you have any suggestions or find problems with this project, welcome to submit feedback through the Issues function on GitHub. Also, you are welcome to contribute to the project by submitting a Pull Request.
