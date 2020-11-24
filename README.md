# InfinityEleNa



Steps to run the backend server(Assuming this is a fresh ubuntu 20.04.1)
1. Install git 
```
sudo apt install git;
```

2. Clone the repository. Enter your git username and password
```
git clone https://github.com/koushikrbukkasamudram/InfinityEleNa.git;
```

3. Install anaconda from the website(https://docs.anaconda.com/anaconda/install/linux/). You can skip step two and the last step. Please install this carefull and check by running ```conda``` to verify if the conda is installed well.

4. Install make
```
sudo apt install make;
```

5. Navigate into InfinityElena directory. Install osmnx environment. The commands are packaged into make file under the create. This can be run by the command.
```
cd InfinityElena;
make create;
```

6. Change the environment to osmnx environment using the command
```
conda init bash;
conda activate CS520-InfinityEleNa;
```

7. Install the python dependencies by running
```
make install
```

8. Navigate into the backend folder and start the backend server
```
cd backend;
python manage.py runserver
```

Steps to run frontend
- cd into the folder frontend/my-maps-project
- run the command 'npm install --save-dev @angular-devkit/build-angular'
- run ng serve
- Open your browser on http://localhost:4200/
- Access the application
