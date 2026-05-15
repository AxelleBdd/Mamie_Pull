# 🧶 MamiePull

> 👥 Individual project  
> 💻 Website created for a family member  
> 🎓 Project for my RNCP professional title  

🚧 **Status:** Work in progress

## 📚 Project Context

To find a fulfilling activity during retirement, the client wants to sell handmade knitted clothes for babies young children and baby dolls.  
MamiePull aims to highlight handmade products while keeping a personal and human approach. <br>
The project provides an online showcase for handcrafted creations, allowing visitors to discover products, models, and get in touch easily.

## 🎯 Project Objectives

- Display the latest knitted creations
- Showcase the different available models
- Display customer feedback and testimonials
- List markets and events where the creator is present
- Provide an easy contact solution for customers

### Constraints

- ❌ No online payment system  
  (Items are handmade on demand and adapted to each customer)
- ✅ Contact section or form to improve customer experience

## 🛠️ Used Stack

### Frontend

- Vue.js 3
- Pinia
- HTML / CSS Tailwind
- Vite

### Backend

- Python
- Django
- PostgreSQL

### Tools

- Docker

## ⚙️ Installation & Setup

This project uses **Docker** for local development.

### Prerequisites

- Docker

### Clone repository

```
git clone [repository url]
```

### Environment Variables

The project uses:

- A global `.env` file
- A frontend-specific `.env` file

See the .env.example to make your own .env files

### Run the project

```bash
docker-compose up --build 
```

## ✨ Features

### Current Implementation

- **Homepage**: Project showcase with layout
- **Product Management**: Display and browse products from the backend
- **User Authentication**: Sign up and sign in functionality
- **User Profile Management**: View and edit user profile information
- **Product Browsing**: Filter products by category, view detailed information and search by title
- **Admin Dashboard**: Add, edit, and delete products (staff only)
- **Contact Feature**: Contact button for product inquiries
- **Responsive Design**: Built with Tailwind CSS for mobile and desktop compatibility

### Planned Features

- **Favorites**: Allow users to save and manage favorite products
- **News & Updates**: Display site news and updates
- **Testimonials**: Customer feedback and reviews section
- **Events & Markets**: List markets and events where the creator is present

## 🧪 Tests

Backend tests have been implemented for:

- User models and authentication
- Product models and views
- Category models

Run tests with: `docker-compose exec backend python manage.py test`

## 🔄 Continuous Integration

This project uses **GitHub Actions** for automated testing and code quality assurance.

### Backend Pipeline (`backend.yml`)

Triggered on:
- Push to `main` branch (backend/ changes)
- Pull requests to `main` branch (backend/ changes)

Steps:
- ✅ Python 3.14 environment setup with pip caching
- ✅ PostgreSQL service initialization
- ✅ Dependency installation
- ✅ Database migrations
- ✅ Automated test suite execution

### Frontend Pipeline (`frontend.yml`)

Triggered on:
- Push to `main` branch (frontend/ changes)
- Pull requests to `main` branch (frontend/ changes)

Steps:
- ✅ Node.js 20 environment setup with npm caching
- ✅ Dependency installation
- ✅ Automated test suite execution

## 🤝 Contribution

This is a **private project** developed for a professional certification.  
External contributions are **not accepted**.
