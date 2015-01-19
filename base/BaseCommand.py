__author__ = "Samuele Dell'Angelo (Red Hat)"
__author__ = "Andrea Battaglia (Red Hat)"

class BaseCommand:

    #readonly vars
    _clipath = "/bin/jboss-cli.sh"
    _cliconn = "-c"
    _clicontr = "--controller="
    _cliuser = "--user="
    _clipwd = "--password="
    _clisg = "/server-group="
    _clidpmt = "/deployment="
    _clisgs = "--server-groups="
    _clirname = "--runtime-name="
    _cliname = "--name="

    #write vars
    _complPath = ""
    _complContr = ""
    _complUser = ""
    _complPwd = ""

    def execute(self, jbossHome, controller, user, password):
        raise NotImplementedError()

    def fillParameters(self, jbossHome, controller, user, password):
        self._complPath = jbossHome+self._clipath
        self._complContr = self._clicontr+controller
        self._complUser = self._cliuser+user
        self._complPwd = self._clipwd+password