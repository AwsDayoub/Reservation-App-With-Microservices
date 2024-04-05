## Description

The Reservation App is a microservices-based application, where the project is divided into several services including 
users, hotel, restaurant, event, car, payment, and notification. These services communicate with each other using 
HTTP requests facilitated by the Requests library. The app calls APIs asynchronously using threading to enhance 
performance and responsiveness.
This versatile and user-friendly application simplifies the process of making and managing reservations for various 
services. Whether it's booking a table at a restaurant, reserving a hotel room, renting a car, or securing a spot for an 
event, our app offers a seamless experience for both users and service providers.


## Features
1. CRUD operations: The app provides full CRUD (Create, Read, Update, Delete) functionality, allowing users to create, view, modify, and delete reservations as needed. This ensures complete control and flexibility over the reservation management process.
2. Task scheduling using celery: Leveraging the power of Celery, the app enables efficient task scheduling and background processing. This feature ensures smooth execution of time-sensitive operations, such as sending reminders, updating availability, or performing automated tasks related to reservations.
3. Real time notifications using webscockets: The app utilizes Websockets technology to deliver real-time notifications to users. Whether it's confirming a reservation, notifying about availability changes, or sending reminders, users receive instant updates without needing to manually refresh the app. This enhances the overall user experience and improves communication between users and service providers.


## Installation
1. clone the repo to your local machine
2. run docker
3. redirect to the docker-compose file directory
4. run docker-compose up


## Class Diagram
![Main](https://github.com/AwsDayoub/Reservation-App-With-Microservices/assets/93884262/8c06131c-5098-403e-a18c-042586f16bc7)

## Documentation
1. open your browser
2. search for http://127.0.0.1:8000/schema/docs
