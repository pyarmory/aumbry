import io
import sys


class OutputCapture(list):
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self._stdoutio = io.StringIO()
        sys.stderr = self._stderrio = io.StringIO()

        return self

    def __exit__(self, *args):
        self.extend(self._stdoutio.getvalue().splitlines())
        self.extend(self._stderrio.getvalue().splitlines())

        del self._stdoutio
        del self._stderrio

        sys.stdout = self._stdout
        sys.stderr = self._stderr
