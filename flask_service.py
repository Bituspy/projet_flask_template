import time
import win32serviceutil
import win32service
import win32event
import servicemanager
from subprocess import Popen
from waitress import serve
from app import app  # Import the Flask app from app.py

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask Application Service"
    _svc_description_ = "Runs the Flask application as a Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        """ Stop the service """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()  # Stop the process if needed
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """ Start the service and run the Flask app """
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.run()

    def run(self):
        """ Run the Flask app using Waitress WSGI server in a separate process """
        try:
            # Introduce a delay to give the system more time to initialize
            time.sleep(5)  # Wait for 5 seconds before starting the Flask app

            # Use the Python executable from the venv
            python_executable = r"C:\TalendInsightApp\venv\Scripts\python.exe"  # Path to your Python executable in venv
            flask_app = r"C:\TalendInsightApp\flask_service.py"  # Path to this script (flask_service.py)

            # Start the Flask app using a separate process
            self.process = Popen([python_executable, flask_app])  # This launches the Flask app in the background

            # Log that the process was started
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                ("Flask app started successfully", "")
            )

        except Exception as e:
            # Log any exception that occurs
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_ERROR_TYPE,
                servicemanager.PYS_SERVICE_FAILED,
                (f"Error starting Flask app: {str(e)}", "")
            )

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FlaskService)
