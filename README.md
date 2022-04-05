# My Fitness
> A place to track my Running, Hiking, and Biking.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)


## General Information
- Track totals and averages for cardio fitness.
- Track wear and tear on my equipment.
- Make sure I meet my yearly goals.
- I wanted to try and make a multi-screen tkinter project.


## Technologies Used
- Python 3.9.9
- Sqlite3
- re (Regular Expressions)
- Pickle
- colorama (Non-GUI Version)


## Features
List the ready features here:
- Automaticly creates a table for the current year if one doesn't exist.
- The Main Screen has a tree view of the current years workouts.
- Totals for each category tracked are at the top.
![HomeScreen](https://user-images.githubusercontent.com/94538153/161746344-7299a414-d32d-4d6e-a990-8553b801c74c.png)
- Add and Edit is where you enter the information.
- The pace is automatically calculated.
- After selecting an event, the equipment list will populate. Or add new in equipment in the entry field.
![AddEditScreen](https://user-images.githubusercontent.com/94538153/161746595-52de54ba-e730-4c9b-bd28-fa33a541bb0c.png)
- The data screen lets you see Yearly totals of each event.
- Or view the monthly totals of each category.
![DataScreen1](https://user-images.githubusercontent.com/94538153/161746692-20d1048d-e34e-4534-b78e-ecf30ab5f792.png)
![DataScreen2](https://user-images.githubusercontent.com/94538153/161746857-3aea4e38-daf6-40ab-a855-6877b66ebb4d.png)
- The PT screen uses a pickle file with 366 calesthenic workouts.
![PtScreen](https://user-images.githubusercontent.com/94538153/161747059-387e4b3e-e1f8-4480-ac7e-33e35116f462.png)


## Setup
- I used [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&gl=US) to use it on my phone.
- You will need the [year_pt](https://github.com/Babaganoush07/fitness/blob/main/year_pt.pkl) pickle file for the Daily PT to work.


## Project Status
Project is: _complete_. 


## Room for Improvement
I need to get better at sizing in tkinter. That took up a lot of my time.

## Acknowledgements
- I got most of my info from [John Elder Codemy.com YouTube](https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV).
- The PT plan from [Stew Smith](https://www.docdroid.net/OZAgQjt/259238051-52-week-training-course-pdf).
- Got the README template from [ritaly](https://github.com/ritaly/README-cheatsheet).
