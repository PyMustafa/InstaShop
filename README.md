# InstaShop
## Django E-Commerce Project

InstaShop is a full-featured e-commerce platform built with Django, designed for scalability and ease of use. With a modern aesthetic provided by Bootstrap and dynamic interactivity facilitated through AJAX, this robust system provides a streamlined shopping experience.

## Basic Features

- Registration using email address
- Custom Admin dashboard
- Search Functionality
-  dynamic Shopping Cart
- Order Filtering

## Technical Stack

- **Backend**: Django handles backend operations.
- **Frontend**: Bootstrap for styling, AJAX for dynamic content loading.
- **Dependency Management**: Poetry for simpler package management and reproducible builds.

## Quick Start Guide

To get InstaShop running on your local machine, follow these steps:

**1. clone Repository**
   ```bash
   git clone https://github.com/PyMustafa/InstaShop.git
   cd instashop
   ```
   rename the **.env.example** file found in the root directory of the project to **.env** and update the environment variables accordingly.

**2. Setup Virtual Environment**
- **using poetry**
   
   install poetry & Create virtual environment
   ```bash
   pip install poetry
   poetry init
   poetry install
   ```
   Activate Your Virtual Environment
   ```bash
   poetry shell
   ```

- **using virtualenv**  

   ```bash
   virtualenv venv
   ```
   In Linux or Mac, activate the new python environment
   ```bash
   source venv/bin/activate
   ```
   Or in Windows
   ```bash
   .\venv\Scripts\activate
   ```
   Confirm that the env is successfully selected
   ```bash
   which python
   ```
   install the requierments
   ```bash
   pip install -r requirements.txt
   ```

**3. Migrate & Start Server**
   
   migrate
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   Create superuser
   ```bash
   python manage.py createsuperuser
   ```
   Start Server
   ```bash
   python manage.py createsuperuser
   ```
Navigate to http://localhost:8000/admin/
## 🔗 Links
check me on

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mustafaahassan/)



## License

InstaShop is licensed under [MIT](https://choosealicense.com/licenses/mit/) License

