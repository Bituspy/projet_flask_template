import win32serviceutil
import win32service
import win32event
import servicemanager
from waitress import serve
from app import app  # Import the Flask app from app.py

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask Application Service"
    _svc_description_ = "Runs the Flask application as a Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        """ Stop the service """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
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
        """ Run the Flask app using Waitress WSGI server """
        # Serve the Flask app with waitress
        serve(app, host='0.0.0.0', port=5000)  # Update port if needed

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FlaskService)
