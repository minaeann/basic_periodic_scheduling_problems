# Basic Periodic Scheduling Problems

**Authors**: Anna Minaeva (<minaevaana@gmail.com>), Zdenek Hanzalek (<Zdenek.Hanzalek@cvut.cz>)

This is the set of basic periodic scheduling problem implementations in Python using SMT solver [Microsoft Z3](https://github.com/Z3Prover/z3) distributed under the terms of the GNU General Public License. 

## Contents

- **single_resource.py** - problem on a single resource described in Subsection 2.1.
- **parallel_identical_resources.py** - problem on a parallel identical resources without preemption and migration described in Subsection 2.2.
- **dedicated_resources.py** - problem on dedicated resources with precedence constraints without preemption and migration described in Subsection 2.3.
- **dedicated_resources_weighted_latency.py** - problem on dedicated resources with precedence constraints without preemption and migration and minimization of weighted end-to-end latency described in Subsection 2.3.

## Installation

To run any of the implementations, you need to install/bind Z3 library. Here we provide multiple ways to install Microsoft Z3:

1. Either use `pip` from Terminal/Shell/Command Prompt

    ```bash
    pip install z3-solver
    ```

2. or install Microsoft Z3 in your IDE (e.g., PyCharm) if it provides this option. 

If succeeded, be sure to add `%Z3_instalation_folder%\bin` into your library path (in macOS, it is done by setting Z3_LIBRARY_PATH variable to this folder)

3. If neither of these options suceedeed:

	a. Download the prebuilt version according to your operation system from [git](https://github.com/Z3Prover/z3/releases).

	b. Set `Z3_LIBRARY_PATH` (macOS, Linux) or `PATH` (Windows) system variables to bin directory of z3 project folder 
	(`%Z3_instalation_folder%/bin`). You can set it locally for each run of the project in your IDE (e.g., PyCharm) under `Debug Configurations -> Environment Variables`.

	c. Make sure that python version 3.* is installed on your machine. (`python -V`, `python3 -V`).

	d. Then, run it in IDE or in Terminal/Shell as

    ```bash
    python3 single_resource.py
    ```

	e. If it still does not work, try copying `%Z3_instalation_folder%/bin/python/z3` folder to your project folder or copy	files of this project to `%Z3_instalation_folder%/bin/python`.

If failed, try out [these instructions](http://www.cs.utexas.edu/users/moore/acl2/manuals/current/manual/index-seo.php/SMT____Z3-INSTALLATION?path=3335/4090/497/1167) as well.


Finally, when Microsoft Z3 is installed, you can run it in the command line as 

```bash
python <fileName> 
```

## Citing

If you find this software useful for your research or you create an algorithm
based on this software, please cite our original paper in your publication list.

- Minaeva, A - Hanzálek, Z. : Survey on Periodic Scheduling for Time-Triggered Hard Real-Time Systems, ACM Computing Surveys, 2020.
