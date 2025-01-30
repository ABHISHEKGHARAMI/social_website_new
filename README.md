# Image Social Platform


This is a Django-based web application that allows users to bookmark images and other data. It provides authentication features, including social login via Google, Facebook, and Twitter using Django OAuth. The application integrates with a database to store user and bookmark details and supports Redis for caching and background tasks. It is designed to run in a local development environment and can be deployed securely using HTTPS with a reverse proxy setup.



## Features
- User Profile Creation and Deletion,User registration
- Built Authentication System using Django for custom auth for user
- Built in Picture bookmark using the browser, storing it dynamically
- share the 3rd party website to the site using the bookmarklet
- Created the detail view of the image , profile of the user
- Making the image load faster by using the thumbnail of the content
- Adding the Ajax for dynamic system for the user
- Building the follow system for the different users
- Creating the activity stream for the user
- Using the redis for the storing and caching it faster