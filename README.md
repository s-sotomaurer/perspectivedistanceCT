# Perspective Distance Estimation for Camera Trap Photos
This is a tool written in Python for easily estimating distance to objects detected with camera traps.

## Installation and Setup
1. Install Python
    - The tool requires a Python installation (>= 3.11.8), which includes Tk. You can install python from [here](https://www.python.org/downloads/).
    - Be sure to activate the option "add `python.exe` to PATH" and include a `pip` installation.
    - Write down the path location where Python will be installed.

2. Virtual Environment
    - After installing python, you need to set up a [virtual environment](https://docs.python.org/3/library/venv.html) to install the required packages in a non-global path in your machine. To set up a virtual environment, first open the command prompt and input
    
          pip install virtualenv
      
    - Then move to the path you want to set the virtual environment in
    
          cd Documents\example\my_path
    
    - and create a virtual environment using your python installation (replace `C:\Path\To\Python\python.exe` with the actual path of your Python installation from step 1.

          virtualenv --python C:\Path\To\Python\python.exe venv

    - Now you can activate the virtual environment:
  
          .\venv\Scripts\activate

3. Pull Code from GitHub
     - Once you have set up a virtual environment, you can pull or download the code of this project into the same file of the virtual environment

4. Dependencies
    - To install the necessary libraries for using the software, open the command prompt once again, move to the virtual environment and run the following line:

          pip install -r requirements.txt

## Usage
1. Go to your project path

       cd Documents\example\my_path
   
2. Activate virtual environment from the path where it was created

       .\venv\Scripts\activate
   
3. run main file

       venv\main.py


## Documentation
The software can be used and shared. This is a preliminary version and no tests are available. If you want to improve the code, feel free to request a pull.

