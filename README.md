# Patient Management System (Python & SQLite)

This repository contains a university assignment developed for the MSc course **Programming Techniques for Biomedical Data Processing and Analysis**.

The project implements a patient management system using **Object-Oriented Programming and SQLite database**.

---

## Project Description

The application allows the user to manage patient records and medical examinations using a local SQLite database.

The system is implemented in Python using classes and database operations.

---

## Features

- Register new patient
- Update patient information
- Record daily medical examinations
- Display list of patients
- Display patient medical history
- Delete patient records
- Input validation for AMKA and examination values

---

## System Architecture

The application uses the following classes:

**Patient**
- Stores patient information (AMKA, first name, last name)

**Examination**
- Stores examination data such as pressure, pulses, temperature and oxygen level

**ClinicApp**
- Handles database operations
- Manages patient records and examinations
- Provides the console menu interface

---

## Technologies Used

- Python
- SQLite3
- Object-Oriented Programming
- SQL
- Console Interface

---

## Database Structure

The system creates two database tables:

**patients**
- amka (primary key)
- first_name
- last_name

**examinations**
- id
- amka
- date
- shift
- pressure
- pulses
- temperature
- oxygen

---

## Author

Christos Dionysios Desyniotis  
MSc Biomedical Informatics
