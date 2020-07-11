This is the set of basic periodic scheduling problem implementations in Python using SMT solver Microsoft Z3 distributed under the terms of the GNU General Public License. 

Authors: Anna Minaeva (minaevaana@gmail.com), Zdenek Hanzalek (Zdenek.Hanzalek@cvut.cz)

single_resource.py - problem on a single resource described in subsection 2.1.
parallel_identical_resources.py - problem on a parallel identical resources without preemption and migration described in subsection 2.2.
dedicated_resources.py - problem on dedicated resources with precedence constraints without preemption and migration described in subsection 2.3.
dedicated_resources_weighted_latency.py - problem on dedicated resources with precedence constraints without preemption and migration and minimization of weighted end-to-end latency described in subsection 2.3.

—————————————————————————————————————————————————————————————————————

To run any of the implementations, you need to install/bind Z3 library. Here we provide multiple ways to install Microsoft Z3:

1. Run >>pip install z3-solver in Terminal/Shell/Command Prompt. or

2. Install Microsoft Z3 in your IDE (e.g., PyCharm) if it provides this option. 

If succeeded, be sure to add %Z3_instalation_folder%\bin into your library path (in macOS, it is done by setting Z3_LIBRARY_PATH variable to this folder)

3. If neither of these options suceedeed:

	a. Download the prebuilt version according to your operation system from https://github.com/Z3Prover/z3/releases.

	b. Set Z3_LIBRARY_PATH (macOS, Linux) or PATH (Windows) system variables to bin directory of z3 project folder 
	(%Z3_instalation_folder%/bin). You can set it locally for each run of the project in your IDE (e.g., PyCharm) under 		Debug Configurations -> Environment Variables.

	c. Make sure that python version 3.* is installed on your machine. (python -V, python3 -V).

	d. Then, run it in IDE or in Terminal/Shell as >>python3 single_resource.py.

	e. If it still does not work, try copying %Z3_instalation_folder%/bin/python/z3 folder to your project folder or copy 		files of this project to %Z3_instalation_folder%/bin/python.

If failed, try out these instructions as well: http://www.cs.utexas.edu/users/moore/acl2/manuals/current/manual/index-seo.php/SMT____Z3-INSTALLATION?path=3335/4090/497/1167.


Finally, when Microsoft Z3 is installed, you can run it in the command line as python <fileName> 

——————————————————————————————————————————————————————————————————————

Remark:

If you find this software useful for your research or you create an algorithm
based on this software, please cite our original paper in your publication list.


Minaeva, A - Hanzálek, Z. : Survey on Periodic Scheduling for Time-Triggered Hard Real-Time Systems.


