# Kalendario - Modern Scheduling Platform

![Kalendario](https://img.shields.io/badge/Kalendario-Scheduling%20Platform-blue)
![React](https://img.shields.io/badge/React-17.0.2-blue)
![Django](https://img.shields.io/badge/Django-3.1.13-green)
![TypeScript](https://img.shields.io/badge/TypeScript-4.2.4-blue)

Kalendario is a full-stack scheduling platform that demonstrates modern web development practices and technologies. This project showcases a robust architecture combining a React TypeScript frontend with a Django REST Framework backend.

## 🚀 Features

- **Modern Frontend**
  - Built with React 17 and TypeScript
  - Redux for state management with Redux Toolkit
  - Responsive design using Reactstrap and Bootstrap
  - Calendar integration with react-big-calendar
  - Form handling with Formik and Yup validation
  - Internationalization support with react-intl

- **Robust Backend**
  - Django REST Framework API
  - JWT Authentication
  - Celery for background tasks
  - PostgreSQL database
  - Stripe integration for payments
  - Social authentication (Facebook)
  - Cloudinary integration for media storage

## 🛠️ Tech Stack

### Frontend
- React 17
- TypeScript
- Redux Toolkit
- React Router
- Formik & Yup
- Reactstrap
- SCSS
- Firebase Hosting

### Backend
- Django 3.1
- Django REST Framework
- Celery
- PostgreSQL
- Redis
- Stripe API
- Cloudinary
- Gunicorn

## 🏗️ Project Structure

```
kalendario/
├── frontend/           # React TypeScript application
│   ├── src/           # Source code
│   ├── public/        # Static files
│   └── package.json   # Frontend dependencies
│
└── backend/           # Django application
    ├── app_auth/      # Authentication module
    ├── billing/       # Payment processing
    ├── scheduling/    # Core scheduling logic
    ├── customers/     # Customer management
    └── requirements.txt # Backend dependencies
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- PostgreSQL
- Redis

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔑 Key Features

- **Authentication & Authorization**
  - JWT-based authentication
  - Social login integration
  - Role-based access control

- **Scheduling System**
  - Interactive calendar interface
  - Appointment management
  - Timezone support
  - Recurring events

- **Payment Processing**
  - Secure Stripe integration
  - Subscription management
  - Payment history tracking

- **User Management**
  - Customer profiles
  - Service provider management
  - Admin dashboard

## 🎯 Development Highlights

- Implemented TypeScript for enhanced type safety and better developer experience
- Built a scalable microservices architecture
- Integrated multiple third-party services (Stripe, Cloudinary, etc.)
- Implemented comprehensive testing suite
- Set up CI/CD pipeline with GitHub Actions
- Deployed on Firebase (Frontend) and Heroku (Backend)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact

Feel free to reach out for any questions or collaboration opportunities!

---
*Built with ❤️ using modern web technologies*
