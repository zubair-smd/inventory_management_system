Inventory_management_system

A cloud-based inventory management system developed with Django and AWS services. This project aims to automate inventory tracking, order management, and reporting to help small and medium-sized enterprises (SMEs) manage their operations efficiently. The system supports real-time stock updates, low-stock notifications, and provides detailed reports on sales, inventory, and order status.

Features include real-time inventory management that tracks stock levels and updates inventory in real-time, low-stock notifications that provide automated alerts when stock levels fall below a predefined threshold, order management with an intuitive interface to easily view, update, and track order statuses, reporting to generate detailed reports on stock levels, sales, order statuses, and other metrics, and user authentication with secure login and sign-up functionality with role-based access control.

The technology stack includes Django for web framework rapid development, AWS services for hosting and cloud infrastructure including Amazon EC2 for application deployment and hosting, Amazon S3 for static file hosting (CSS, images), Amazon RDS for storing inventory and order data, AWS Lambda for serverless functions triggering low-stock alerts, AWS CodeDeploy for automated deployment, and AWS CodePipeline for continuous delivery. The system also uses PostgreSQL for storing application data (orders, products, etc.), Bootstrap for front-end UI components, and Chart.js for visualizing inventory and order data in charts.

To install the project locally, Installation Instructions:
1. Clone the repository: git clone https://github.com/zubair-smd/Django-Inventory-mgt.git
2. Navigate to project directory
3. Create virtual environment: python3 -m venv venv
4. Activate virtual environment:
   - For Windows: venv\Scripts\activate
   - For Linux/Mac: source venv/bin/activate
5. Install dependencies: pip install -r requirements.txt
6. Set up database: python manage.py migrate
7. Create superuser: python manage.py createsuperuser
8. Start development server: python manage.py runserver
9. Access application: http://127.0.0.1:8000/

For AWS configuration, set up Amazon EC2 for application hosting by launching an instance with appropriate configurations and security groups. Configure Amazon S3 for static file hosting, set up Amazon RDS for database hosting and update the settings accordingly. AWS Lambda functions handle low-stock notifications with a simple function that monitors inventory levels. AWS CodeDeploy and CodePipeline are implemented for automated deployment and continuous delivery, streamlining the development to production workflow.

The Lambda integration for low-stock notifications is implemented with a Python function that queries products with quantities below a threshold and generates alerts. The CI/CD pipeline uses AWS CodePipeline to automate the build and deployment process, pulling code from GitHub, running tests, and deploying to EC2 instances through CodeDeploy.

Once running, users can access features including user authentication, a comprehensive dashboard showing real-time inventory and order statistics, product management for adding, editing, or deleting products, inventory tracking, order management from pending to completed status, and detailed reporting capabilities for sales, inventory levels, and order statuses.
