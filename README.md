> **Warning**
> Although this project is running stable it needs further work before it can be used in a productive environment. Especially the frontend is based on an outdated repository.

# brDashboard
brDashboard is a temperature monitoring and controlling application that supports real-time data.

## Installation
### Dashboard
To start a local version of brDashboard, you have to build the dashboard first, which is based on https://www.creative-tim.com/product/vue-black-dashboard-pro.
To build the dashboard, run `npm run build` in the `dashboard` folder. This creates the frontend-app in the folder `dashboard/dist`. Notice that you can also run `npm run dev` if you want to further work on the dashboard-frontend.

**Note**
The dashboard is currently only tested on Node 14. Please make sure that you run the correct version with `node --version` and if not use `nvm` to install node 14 (or install node 14 dierctly).

### Admin-Frontend

Once the dashboard is built, you can run the webserver.

1. (Optional) Make and activate a virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install the requirements: `pip install -r requirements.txt`
3. Specify flask app: `export FLASK_APP=admin:app`
4. Initiate the database: `flask db upgrade head`
5. (Optional) Add test user: `flask create-user <username> <password>`
6. Start server: `flask run`
7. Go to `http://localhost:5000/` in your browser and login with the username.

> **Note**
> These steps are the necessary steps for a minimal setup. It will use `sqlite` as database and will also use this database to store any values received by sensors. `SQL` is not the optimal choice for time-series and alternatively it is also possible to use https://www.influxdata.com/ to store time series values. If you want to use Influx, adapt the `provider` in `DATA_HANDLER` of the config in `config.py` accordingly.

> **Warning**
> Additionally to the database choice, the default config is not designed for production! If you want to use the control suite in a productive environment it is crucial to adapt `config.py` accordingly!

## Docker

Alternatively, you can set up the application with docker. Simply run `docker build -t tempmonitor .` and then `docker run -p 8080:8080 tempmonitor`. You should be able to access the app under `http://localhost:8080`. By default, a user with the credentials `test` and pw `123456` is added.

> **Warning**
> The Docker Image is not production ready! It is crucial to change the default user in `entrypoint.sh` and once the app is running to add another user and delete the default user.
> Furthermore, there is no file persistency, so any data will be lost once the docker container stops running. To implement that, you have to map a volume to the container or use an external DB and adapt the SQLAlchemy string accordingly.


## Usage

When the server is running you can add a new device in the Admin-Panel under Devices. Once you've added a device, you can add Sensors to it. A Sensor can either be a simple "Read"-sensor which only returns measured values or a "Controller", which also allows regulating the values. 

In the "Control"-Panel, you can see and regulate the received values of the devices and sensors. In order to switch between the "Control" and the "Admin" panel, you can click on the human icon in the top right corner.

The specifications for the implementation of new sensors are given in this repo: https://github.com/vinzenz-muser/brDeviceSensor. Alternatively, you can navigate to `/static/mock.html` where an example device is implemented. You need to fill in the API-Key, the sensor ids and the url if necessary. Once you submit, random values will be sent to the server.

