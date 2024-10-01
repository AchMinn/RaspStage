# SmartHome Dashboard

**SmartHome Dashboard** is a Django web application designed to log and visualize changes in a smart home environment. This application tracks various devices and their usage, providing insightful dashboards to monitor and analyze device consumption over time.

## Features

- **Device Management**: Add, update, and manage smart home devices, including lamps, plugs, and climate controls.
- **Consumption Tracking**: Record and visualize consumption data from devices.
- **Dashboard Visualizations**: Interactive charts display consumption data per device and per device type.
- **Date Range Filtering**: Filter data based on the last updated timestamp to focus on specific periods.
- **Change Logging**: Keep a history of changes made to device configurations and measurements.

## Project Setup

### Prerequisites

- Python 3.8+
- Django 3.2+
- (If any help needed with installing, open a new issue)

### Installation

1. **Clone the Repository**

	```bash
   git clone https://github.com/AchMinn/RaspStage.git
   cd RaspStage
 
2. **Create a Virtual Environment (if needed)**

	```bash
	python -m venv venv
	source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
 
3. **Install dependecies**

	```bash
	pip install -r requirements.txt

4. **Create a .env File**
   	```bash
    	Manually create a .env file with the necessary environment variables. ( See Settings.py to know what variables are needed )
    
5. **Run migrations**

	```bash
 	python manage.py migrate

6. ** Create the ssl certificate "in your root directory containing manage.py"**

 	```bash
 	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem


7. **Create a superuser**
   	```bash
    	python manage.py createsuperuser
    
8. **Run the Development Server Locally**
   	```bash
    	python manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem

8. **Run the Production Deployement Server Locally**
   	```bash
    	gunicorn --bind 0.0.0.0:8000 --certfile cert.pem --keyfile key.pem WebPageDjango.wsgi:application

Access the application at http://{ip address}:8000/

## Usage

- **Access the Dashboard**: Navigate to the dashboard page at `/measurements/` to view device consumption data.
- **Filter Data**: Use the range inputs to filter records.
- **View Charts**: Interactive charts will update based on the selected date range and display consumption statistics.
- **Add, control and edit Devices**: Create new devices or/and control the already existing devices in the smarthome.

## Models

### Room

Represents a physical room in the smart home, e.g., salon, cuisine, etc.

- `name`: Name of the room.
- `description`: Optional description of the room.

### Device

Represents a smart home device.

- `name`: Name of the device.
- `model`: Model of the device.
- `description`: Optional description of the device.
- `last_connected`: Timestamp of the last connection.
- `room`: Foreign key linking to the `Room` model.
- `is_active`: Status indicating if the device is currently active.
- `device_type`: Type of the device (e.g., lamp, plug, climate control).
- `intensity`: Optional field representing device intensity.

### Measurement

Logs measurements from devices.

- `name`: Name of the measurement.
- `device`: Foreign key linking to the `Device` model.
- `last_updated`: Timestamp when the measurement was last updated.
- `value`: Measurement value.

### History

Tracks changes in your smarthome web app.

- `table_name`: Name of the table where the change occurred.
- `record_id`: ID of the changed record.
- `field_name`: Name of the field that was changed.
- `old_value`: Old value of the field.
- `new_value`: New value of the field.
- `updated_at`: Timestamp when the change was made.
- `updated_by`: User who made the change.
- `message`: Optional message about the change.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project’s coding standards and passes all tests.

## Contact

For questions or feedback, please contact:

- **Email**: achraf.elminor@e-polytechnique.ma
- **GitHub**: [AchMinn](https://github.com/AchMinn)

