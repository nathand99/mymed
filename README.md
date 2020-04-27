# Weekly-Cri-Sesh
RUN INSTRUCTOINS
1. Create an environment in the root of the folder (Weekly-Cri-Sesh) 
(in the example the enviroment will be called env)
	virtualenv env

2. Activate the environment
	source env/bin/activate

3. Install the requirements
	pip3 install -r requirements.txt

4. Run the application
	python3 run.py 

5. Open a browser and direct to either;
	i. http://localhost:5010/
	ii. http://127.0.0.1:5010/

6. Use website

TROUBLESHOOTING
1. If python3 run.py produces the error ModuleNotFoundError: No module named 'flask'.
	i) Environment is not activated
		Solve by running 'source env/bin/activate'
	ii) Environment does not have requirements installed 
		Solve by running 'pip3 install -r requirements.txt'
2. Server is running but I can't access the website.
	i) Localhost port is being used by another process.
	 	Solve by closing server, opening run.py and changing port to another number and try again