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

## 🚀 Usage

At this stage:

- The homepage is displayed but not complete
- Navigation bar and search bar are displayed but not fully functionnal
- Products generated from the backend are fetched and shown
- User authentication is implemented (sign up / sign in)
- Users can browse products by category and view details

🔧 API documentation and endpoints will be added later.

## ✨ Features

### Existing Features (Frontend & Backend)

- Homepage layout
- Display of products from the backend
- User authentication (sign up / sign in)
- Browse products by category
- View product details

### Planned Features

#### User Features

- Manage favorite products
- View site news and updates
- Search functionality for products
- Display customer feedback and testimonials
- List markets and events

#### Admin Features

- Add, edit, and delete products
- Manage news and updates

## 🧪 Tests

Backend tests have been implemented for:

- User models and authentication
- Product models and views
- Category models

Run tests with: `docker-compose exec backend python manage.py test`

## 🤝 Contribution

This is a **private project** developed for a professional certification.  
External contributions are **not accepted**.
