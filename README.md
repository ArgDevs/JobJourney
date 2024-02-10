
# JobJourney

## Overview

JobJourney is a comprehensive solution designed to manage job applications and interview preparations efficiently. Combining a powerful Django REST backend with a dynamic React frontend, this project streamlines the process of tracking job applications, job leads, CVs, and cover letters, offering users a seamless experience from application tracking to interview preparation.

## Features
- **Job Application Management**: Easily add, update, and track the status of job applications.
- **Interview Preparation**: Store notes, questions, and resources for interview preparation.
- **Dynamic Dashboard**: View and manage your job applications and leads with an interactive dashboard.
- **RESTful API**: Secure and scalable backend architecture using Django REST Framework.
- **Responsive Design**: A modern, responsive frontend built with React, ensuring a great experience across devices.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Frontend**: React, Bootstrap (for styling)
- **Database**: PostgreSQL (recommended for production), SQLite (for development)
- **Deployment**: Configurations for both development and production environments

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 14+
- npm or yarn

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ArgDevs/JobJourney.git
   cd JobJourney
   ```

2. **[Backend Setup](backend/README.md)**

3. **[Frontend Setup](frontend/README.md)**

4. **Access the Application**
   - Open your browser and navigate to `http://localhost:3000` to view the React frontend.
   - The Django API is accessible at `http://localhost:8000/api`.

### Docker compose local setup

1. Run the local stack with docker compose
```bash
docker-compose up -d 
```

## Contributing
We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

## License
This project is licensed under the [MIT License](https://github.com/ArgDevs/JobJourney/LICENSE.md).

## Authors
- **Osvaldo Demo** - *Initial work* - [borland667](https://github.com/borland667)
