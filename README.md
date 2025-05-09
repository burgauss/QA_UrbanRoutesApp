# qa project Urban Route test
The application Urban routes is an application designed for finding a driver in case you want to move from point A to point B, it allows for more functionality for example:
- Different types of tarfis
- Option to send a message to the driver
- possibility to pay by cash or card
- extra selection of commodities like ice cream or blankets


This project test the well functioning of the Urban Routes Project, it test for the following behaviors:
1. Configure the address (this part is written for you as an example).
2. Select the Comfort tariff.
3. Fill in the phone number.
4. Add a credit card
5. Write a message to the controller.
6. Order a blanket and tissues.
7. Order 2 ice creams.
8. The modal to find a cab appears.
---
## Dependecies
This project use the following dependecies:
- python 3.12
- selenium
- pytest
---
## Project structure

The project structure contains two files:   

The data.py file contains the data that is used to be evaluated.  
The main.py contains all the tests used.

## How to run the project

In order to run the project, make sure the urban_routes_url contains a valid url and that the server is active.

Also find yourself in the route of the file and you have the dependecies install. then you can run in the console:

pytest main.py

