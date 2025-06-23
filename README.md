# Skill Exchange Platform

A full-stack web application for matching users to exchange skills and learn from each other.

## Demo Video
https://www.youtube.com/watch?v=AH1FVZp8-Ys

## Deployment

- **Backend** and **frontend** are deployed on [Render](https://skill-exchange-1-m2ba.onrender.com/).
- The app uses a free-tier PostgreSQL database on Render, which will be deactivated on **2025-07-23**.
- **AI Usage Note:**  
  This is a personal project, so the deployed backend uses my own Gemini API key (set as an environment variable in Render). The Gemini API free tier allows up to 50 requests per day; if this quota is exceeded, AI-powered features will be temporarily unavailable until the quota resets (every 24 hours). If you see that AI features are not working, please try again the next day.
- Feel free to play around with the app using the following credentials:
    - Email: User1@gmail.com
    - Password: 1234

## Problem Statement

Learning new skills can be lonely, costly, and hard to stay motivated. Especially without guidance and support. While many people are eager to share what they know, there's no simple, peer-based way to connect based on shared interests and skills.
Most platforms are built for content delivery, not human connection.
But what if learning felt more like meeting a friend than taking a class?
This project aims to solve that by creating a user-friendly Skill Exchange App, where users match by what they want to learn and teach, then connect, chat, and support each other. 
It makes learning social, fun, and free. Inspired by social matching platforms, the app helps people find partners with complementary skills and shared interests. 
By fostering mutual support and peer-to-peer learning, it turns learning into a social, rewarding experience.

## Project Structure

- `backend/` — Flask, SQLAlchemy, PostgreSQL API
- `frontend/` — React web client
- `docs/` — Documentation

## Quick Start

- **Backend setup:** See [backend/README.md](backend/README.md)
- **Frontend setup:** See [frontend/README.md](frontend/README.md)

## Documentation

- [API Reference](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [AI Integration](docs/SETUP_AI.md)

---

## Demo Screenshots

### Login or Sign Up
![Login or Sign Up](frontend/src/assets/Login%20or%20Sign%20up%20Demo.png)

### How It Works
![How It Works](frontend/src/assets/How%20it%20works%20Demo.png)

### Profile Page
![Profile Page](frontend/src/assets/Profile%20Demo.png)

### Matching Page
![Matching Page](frontend/src/assets/Matching%20Page%20Demo.png)

### Chat
![Chat](frontend/src/assets/Chat%20Demo.png)

### Rating
![Rating](frontend/src/assets/Rating%20Demo.png)
